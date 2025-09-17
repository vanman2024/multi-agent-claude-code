"""Agent pool management for multi-instance orchestration."""

from __future__ import annotations

import logging
import time
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

import psutil

from .config import AgentConfig
from .models import AgentProcess


Provisioner = Callable[[int, AgentConfig], Awaitable[AgentProcess]]
Terminator = Callable[[AgentProcess], Awaitable[None]]


class PoolHealth:
    """Health status of an agent pool."""

    def __init__(
        self,
        *,
        total_instances: int,
        healthy_instances: int,
        unhealthy_instances: int,
        status: str,
        details: Dict[str, Any],
    ) -> None:
        self.total_instances = total_instances
        self.healthy_instances = healthy_instances
        self.unhealthy_instances = unhealthy_instances
        self.status = status
        self.details = details


class AgentStatus:
    """Status of individual agent."""

    def __init__(
        self,
        *,
        instance_id: int,
        status: str,
        pid: int,
        memory_usage: str,
        uptime: str,
        last_activity: str,
    ) -> None:
        self.instance_id = instance_id
        self.status = status
        self.pid = pid
        self.memory_usage = memory_usage
        self.uptime = uptime
        self.last_activity = last_activity


class AgentPool:
    """Manage multiple instances of the same agent type."""

    def __init__(
        self,
        agent_type: str,
        deployment_id: str,
        agent_config: AgentConfig,
        provisioner: Provisioner,
        terminator: Terminator,
    ) -> None:
        self.agent_type = agent_type
        self.deployment_id = deployment_id
        self.agent_config = agent_config
        self._provisioner = provisioner
        self._terminator = terminator
        self.running_instances: List[AgentProcess] = []
        self.logger = logging.getLogger(f"{__name__}.{deployment_id}.{agent_type}")

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    async def scale(self, delta: int) -> Tuple[List[AgentProcess], List[AgentProcess]]:
        """Scale pool size by delta."""

        created: List[AgentProcess] = []
        removed: List[AgentProcess] = []

        if delta > 0:
            created = await self._scale_up(delta)
        elif delta < 0:
            removed = await self._scale_down(abs(delta))

        return created, removed

    async def _scale_up(self, count: int) -> List[AgentProcess]:
        created: List[AgentProcess] = []
        for _ in range(count):
            instance_id = self._next_instance_id()
            process = await self._provisioner(instance_id, self.agent_config)
            self.running_instances.append(process)
            created.append(process)
            self.logger.info(
                "Provisioned %s instance %s (pid=%s)",
                self.agent_type,
                instance_id,
                process.pid,
            )
        return created

    async def _scale_down(self, count: int) -> List[AgentProcess]:
        removed: List[AgentProcess] = []
        for _ in range(min(count, len(self.running_instances))):
            process = self.running_instances.pop()
            await self._terminator(process)
            removed.append(process)
            self.logger.info(
                "Terminated %s instance %s (pid=%s)",
                self.agent_type,
                process.instance_id,
                process.pid,
            )
        return removed

    def register_existing(self, processes: List[AgentProcess]) -> None:
        self.running_instances = processes

    def remove_instance(self, instance_id: int) -> None:
        self.running_instances = [
            proc for proc in self.running_instances if proc.instance_id != instance_id
        ]

    # ------------------------------------------------------------------
    # Monitoring helpers
    # ------------------------------------------------------------------
    async def health_check(self) -> PoolHealth:
        healthy = 0
        unhealthy = 0
        details: Dict[str, Any] = {}

        for process in self.running_instances:
            if process.is_alive():
                healthy += 1
                details[f"instance_{process.instance_id}"] = "healthy"
            else:
                unhealthy += 1
                details[f"instance_{process.instance_id}"] = "unhealthy"

        total = len(self.running_instances)
        if healthy == total and total > 0:
            status = "healthy"
        elif healthy > 0:
            status = "degraded"
        else:
            status = "unhealthy"

        return PoolHealth(
            total_instances=total,
            healthy_instances=healthy,
            unhealthy_instances=unhealthy,
            status=status,
            details=details,
        )

    async def get_instance_status(self, instance_id: int) -> AgentStatus:
        process = self._get_instance(instance_id)
        is_running = process.is_alive()
        pid = process.pid
        memory = self._get_memory_usage(pid) if is_running else "0MB"
        uptime = self._get_uptime(process) if is_running else "0s"
        return AgentStatus(
            instance_id=instance_id,
            status="running" if is_running else "stopped",
            pid=pid,
            memory_usage=memory,
            uptime=uptime,
            last_activity="active" if is_running else "inactive",
        )

    async def restart_instance(self, instance_id: int) -> AgentProcess:
        process = self._get_instance(instance_id)
        await self._terminator(process)
        new_process = await self._provisioner(instance_id, self.agent_config)
        self.remove_instance(instance_id)
        self.running_instances.append(new_process)
        self.logger.info(
            "Restarted %s instance %s (pid=%s)", self.agent_type, instance_id, new_process.pid
        )
        return new_process

    def get_pool_summary(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type,
            "deployment_id": self.deployment_id,
            "target_instances": len(self.running_instances),
            "running_instances": len(self.running_instances),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _get_instance(self, instance_id: int) -> AgentProcess:
        for process in self.running_instances:
            if process.instance_id == instance_id:
                return process
        raise ValueError(
            f"Instance {instance_id} not found in pool {self.agent_type}"
        )

    def _next_instance_id(self) -> int:
        if not self.running_instances:
            return 1
        return max(process.instance_id for process in self.running_instances) + 1

    @staticmethod
    def _get_memory_usage(pid: int) -> str:
        try:
            process = psutil.Process(pid)
            memory_mb = process.memory_info().rss / 1024 / 1024
            return f"{memory_mb:.1f}MB"
        except Exception:
            return "unknown"

    @staticmethod
    def _get_uptime(process: AgentProcess) -> str:
        elapsed = max(0.0, time.time() - process.start_time)
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
