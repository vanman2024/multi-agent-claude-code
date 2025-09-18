"""Persistent state management for AgentSwarm deployments."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

STATE_DIRECTORY_NAME = ".agentswarm"
STATE_FILE_NAME = "state.json"


def _default_state() -> Dict[str, Any]:
    return {
        "deployments": {},
        "last_deployment_id": None,
        "last_updated": None,
    }


class SwarmStateStore:
    """Simple JSON-backed state store for orchestrator metadata."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.state_path = self.base_path / STATE_FILE_NAME
        self._state = self._load()

    # ------------------------------------------------------------------
    # Core persistence helpers
    # ------------------------------------------------------------------
    def _load(self) -> Dict[str, Any]:
        if not self.state_path.exists():
            return _default_state()

        with self.state_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        return _default_state() | data

    def _save(self) -> None:
        self._state["last_updated"] = datetime.now(UTC).isoformat()
        with self.state_path.open("w", encoding="utf-8") as handle:
            json.dump(self._state, handle, indent=2)

    # ------------------------------------------------------------------
    # Deployment management
    # ------------------------------------------------------------------
    def record_deployment(self, deployment: Any) -> None:
        deployments = self._state.setdefault("deployments", {})
        deployments[deployment.deployment_id] = self._serialize_deployment(deployment)
        self._state["last_deployment_id"] = deployment.deployment_id
        self._save()

    def update_deployment(self, deployment_id: str, payload: Dict[str, Any]) -> None:
        deployments = self._state.setdefault("deployments", {})
        if deployment_id not in deployments:
            raise KeyError(f"Deployment {deployment_id} not found")
        deployments[deployment_id].update(payload)
        self._save()

    def remove_deployment(self, deployment_id: str) -> None:
        deployments = self._state.setdefault("deployments", {})
        deployments.pop(deployment_id, None)
        if self._state.get("last_deployment_id") == deployment_id:
            self._state["last_deployment_id"] = next(iter(deployments or []), None)
        self._save()

    def get_deployment(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        deployments = self._state.setdefault("deployments", {})
        payload = deployments.get(deployment_id)
        return json.loads(json.dumps(payload)) if payload else None

    def latest_deployment(self) -> Optional[Dict[str, Any]]:
        deployment_id = self._state.get("last_deployment_id")
        if not deployment_id:
            return None
        return self.get_deployment(deployment_id)

    def list_deployments(self) -> Iterable[Dict[str, Any]]:
        deployments = self._state.setdefault("deployments", {})
        for payload in deployments.values():
            yield json.loads(json.dumps(payload))

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _serialize_deployment(deployment: Any) -> Dict[str, Any]:
        return {
            "deployment_id": deployment.deployment_id,
            "start_time": deployment.start_time,
            "config": deployment.config.to_dict() if hasattr(deployment.config, "to_dict") else {},
            "agents": {
                agent_type: [SwarmStateStore._serialize_process(proc) for proc in processes]
                for agent_type, processes in deployment.agents.items()
            },
        }

    @staticmethod
    def _serialize_process(process: Any) -> Dict[str, Any]:
        payload = {
            "pid": getattr(process, "pid", None),
            "agent_type": getattr(process, "agent_type", None),
            "instance_id": getattr(process, "instance_id", None),
            "command": getattr(process, "command", None),
            "status": getattr(process, "status", None),
            "cwd": getattr(process, "cwd", None),
            "start_time": getattr(process, "start_time", None),
        }
        return {key: value for key, value in payload.items() if value is not None}

    # ------------------------------------------------------------------
    # Convenience accessors used by CLI
    # ------------------------------------------------------------------
    def as_dict(self) -> Dict[str, Any]:
        return json.loads(json.dumps(self._state))
