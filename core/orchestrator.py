"""Main orchestration engine for AgentSwarm deployments."""

from __future__ import annotations

import asyncio
import logging
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .agent_pool import AgentPool
from .config import AgentConfig, SwarmConfig
from .models import AgentProcess, SwarmDeployment
from .state import STATE_DIRECTORY_NAME, SwarmStateStore


class AgentOrchestrator:
    """Coordinates agent processes across deployments."""

    def __init__(
        self,
        *,
        project_root: Optional[Path] = None,
        state_store: Optional[SwarmStateStore] = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(project_root).resolve() if project_root else Path.cwd()
        if state_store is None:
            state_dir = self.project_root / STATE_DIRECTORY_NAME
            self.state_store = SwarmStateStore(state_dir)
        else:
            self.state_store = state_store

        self.pools: Dict[Tuple[str, str], AgentPool] = {}
        self.deployments: Dict[str, SwarmDeployment] = {}

        self._hydrate_from_state()

    # ------------------------------------------------------------------
    # Deployment lifecycle
    # ------------------------------------------------------------------
    async def deploy_swarm(self, config: SwarmConfig) -> SwarmDeployment:
        deployment_id = self._generate_deployment_id()
        self.logger.info("Deploying swarm %s", deployment_id)

        agents: Dict[str, List[AgentProcess]] = {}

        for agent_type, agent_config in config.iter_agents():
            pool = self._ensure_pool(deployment_id, agent_type, agent_config)
            created, _ = await pool.scale(agent_config.get("instances", 1))
            agents[agent_type] = list(pool.running_instances)
            self.logger.debug(
                "Provisioned %s %s instances", len(created), agent_type
            )

        deployment = SwarmDeployment(
            agents=agents,
            config=config,
            deployment_id=deployment_id,
            start_time=datetime.now(UTC).isoformat(),
        )

        self.deployments[deployment_id] = deployment
        self._persist_state(deployment_id)
        return deployment

    async def scale_agents(
        self,
        agent_type: str,
        delta: int,
        *,
        deployment_id: Optional[str] = None,
    ) -> List[AgentProcess]:
        if delta == 0:
            return []

        target_deployment = self._resolve_deployment_id(deployment_id)
        pool = self._get_pool(target_deployment, agent_type)
        created, removed = await pool.scale(delta)

        deployment = self.deployments[target_deployment]
        deployment.agents.setdefault(agent_type, [])

        if delta > 0:
            deployment.agents[agent_type].extend(created)
        else:
            to_remove = {proc.instance_id for proc in removed}
            deployment.agents[agent_type] = [
                proc
                for proc in deployment.agents[agent_type]
                if proc.instance_id not in to_remove
            ]

        self._persist_state(target_deployment)
        self.logger.info(
            "Scaled deployment %s agent %s by %s", target_deployment, agent_type, delta
        )
        return created if delta > 0 else removed

    async def shutdown_deployment(self, deployment_id: str, *, force: bool = False) -> None:
        if deployment_id not in self.deployments:
            raise ValueError(f"Deployment {deployment_id} not found")

        self.logger.info("Shutting down deployment %s", deployment_id)
        deployment = self.deployments[deployment_id]

        for agent_type in list(deployment.agents.keys()):
            pool = self._get_pool(deployment_id, agent_type)
            for process in list(pool.running_instances):
                await self._terminate_agent_process(process, force=force)
            pool.running_instances.clear()
            del self.pools[self._pool_key(deployment_id, agent_type)]

        del self.deployments[deployment_id]
        self.state_store.remove_deployment(deployment_id)

    async def list_deployments(self) -> List[SwarmDeployment]:
        return list(self.deployments.values())

    # ------------------------------------------------------------------
    # Monitoring
    # ------------------------------------------------------------------
    async def health_check(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {}
        for (deployment_id, agent_type), pool in self.pools.items():
            key = f"{deployment_id}:{agent_type}"
            summary[key] = await pool.health_check()
        return summary

    async def get_agent_pool(self, agent_type: str, *, deployment_id: Optional[str] = None) -> Optional[AgentPool]:
        target_deployment = self._resolve_deployment_id(deployment_id, required=False)
        if target_deployment is None:
            return None
        key = self._pool_key(target_deployment, agent_type)
        return self.pools.get(key)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _hydrate_from_state(self) -> None:
        for payload in self.state_store.list_deployments():
            config_dict = payload.get("config", {})
            config = SwarmConfig(
                agents=config_dict.get("agents", {}),
                deployment=config_dict.get("deployment", {}),
                metadata=config_dict.get("metadata", {}),
            )

            agents: Dict[str, List[AgentProcess]] = {}
            deployment_id = payload["deployment_id"]

            for agent_type, entries in payload.get("agents", {}).items():
                processes: List[AgentProcess] = []
                for entry in entries:
                    process = AgentProcess(
                        pid=entry.get("pid", -1),
                        agent_type=agent_type,
                        instance_id=entry.get("instance_id", len(processes) + 1),
                        command=entry.get("command", ""),
                        status=entry.get("status", "unknown"),
                        cwd=entry.get("cwd"),
                        start_time=entry.get("start_time", 0.0),
                    )
                    processes.append(process)

                pool = self._ensure_pool(
                    deployment_id,
                    agent_type,
                    config.agents.get(agent_type, {}),
                )
                pool.register_existing(processes)
                agents[agent_type] = processes

            deployment = SwarmDeployment(
                agents=agents,
                config=config,
                deployment_id=deployment_id,
                start_time=payload.get("start_time", ""),
            )
            self.deployments[deployment_id] = deployment

    def _ensure_pool(
        self,
        deployment_id: str,
        agent_type: str,
        agent_config: AgentConfig,
    ) -> AgentPool:
        key = self._pool_key(deployment_id, agent_type)
        if key not in self.pools:
            async def provisioner(instance_id: int, config: AgentConfig) -> AgentProcess:
                return await self._deploy_agent_instance(
                    deployment_id, agent_type, instance_id, config
                )

            async def terminator(process: AgentProcess) -> None:
                await self._terminate_agent_process(process)

            self.pools[key] = AgentPool(
                agent_type=agent_type,
                deployment_id=deployment_id,
                agent_config=agent_config,
                provisioner=provisioner,
                terminator=terminator,
            )
        return self.pools[key]

    async def _deploy_agent_instance(
        self,
        deployment_id: str,
        agent_type: str,
        instance_id: int,
        config: AgentConfig,
    ) -> AgentProcess:
        command = self._build_agent_command(agent_type, instance_id, config)
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=str(self.project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        agent_process = AgentProcess(
            pid=process.pid,
            agent_type=agent_type,
            instance_id=instance_id,
            command=command,
            cwd=str(self.project_root),
            handle=process,
        )

        self.logger.info(
            "Started %s instance %s for deployment %s (pid=%s)",
            agent_type,
            instance_id,
            deployment_id,
            process.pid,
        )
        return agent_process

    async def _terminate_agent_process(
        self, process: AgentProcess, force: bool = False
    ) -> None:
        if process.handle is not None and process.handle.poll() is None:
            process.handle.terminate() if not force else process.handle.kill()
            loop = asyncio.get_running_loop()
            try:
                await asyncio.wait_for(
                    loop.run_in_executor(None, process.handle.wait),
                    timeout=5,
                )
            except asyncio.TimeoutError:
                process.handle.kill()
        else:
            process.terminate(graceful=not force)

        process.status = "terminated"

    def _build_agent_command(
        self, agent_type: str, instance_id: int, config: AgentConfig
    ) -> str:
        commands = {
            "codex": f'codex exec "Working on instance {instance_id}"',
            "claude": f'claude -p "Working on instance {instance_id}"',
            "gemini": f'gemini "Working on instance {instance_id}"',
            "copilot": f'gh copilot explain "Working on instance {instance_id}"',
        }

        return commands.get(agent_type, f'echo "Unknown agent type: {agent_type}"')

    def _persist_state(self, deployment_id: str) -> None:
        if deployment_id in self.deployments:
            self.state_store.record_deployment(self.deployments[deployment_id])

    def _resolve_deployment_id(
        self, deployment_id: Optional[str], *, required: bool = True
    ) -> Optional[str]:
        if deployment_id:
            return deployment_id
        if self.deployments:
            # Most recent deployment
            return next(reversed(self.deployments.keys()))
        if required:
            raise ValueError("No deployments available")
        return None

    @staticmethod
    def _pool_key(deployment_id: str, agent_type: str) -> Tuple[str, str]:
        return deployment_id, agent_type

    def _get_pool(self, deployment_id: str, agent_type: str) -> AgentPool:
        key = self._pool_key(deployment_id, agent_type)
        if key not in self.pools:
            raise ValueError(
                f"Agent type {agent_type} not found for deployment {deployment_id}"
            )
        return self.pools[key]

    def _generate_deployment_id(self) -> str:
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        suffix = len(self.deployments)
        return f"swarm-{timestamp}-{suffix}"
