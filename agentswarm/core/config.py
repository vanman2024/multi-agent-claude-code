"""Configuration management utilities for AgentSwarm."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import json
import yaml


AgentConfig = Dict[str, Any]

DEFAULT_DEPLOYMENT_CONFIG: Dict[str, Any] = {
    "strategy": "parallel",
    "max_concurrent": 8,
    "timeout": "30m",
}

SUPPORTED_CONFIG_EXTENSIONS = {".yaml", ".yml", ".json"}


def _deep_update(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Return a recursively merged dictionary copy."""

    result = dict(base)
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_update(result[key], value)
        else:
            result[key] = value
    return result


@dataclass(slots=True)
class SwarmConfig:
    """Configuration container for a swarm deployment."""

    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    deployment: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.deployment:
            self.deployment = dict(DEFAULT_DEPLOYMENT_CONFIG)
        else:
            self.deployment = _deep_update(DEFAULT_DEPLOYMENT_CONFIG, self.deployment)
        self.validate()

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_file(cls, file_path: str | Path) -> "SwarmConfig":
        """Load configuration from a YAML or JSON file."""

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        if path.suffix.lower() not in SUPPORTED_CONFIG_EXTENSIONS:
            raise ValueError(
                f"Unsupported config format '{path.suffix}'."
                " Expected one of: .yaml, .yml, .json"
            )

        with path.open("r", encoding="utf-8") as handle:
            if path.suffix.lower() in {".yaml", ".yml"}:
                data = yaml.safe_load(handle) or {}
            else:
                data = json.load(handle) or {}

        return cls(
            agents=data.get("agents", {}),
            deployment=data.get("deployment", {}),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def from_instances(
        cls,
        instance_spec: str,
        *,
        task: Optional[str] = None,
        template: Optional[Dict[str, AgentConfig]] = None,
    ) -> "SwarmConfig":
        """Build a configuration from an instance specification string."""

        if not instance_spec:
            raise ValueError("Instance specification cannot be empty")

        agents: Dict[str, AgentConfig] = {}
        for chunk in instance_spec.split(","):
            token = chunk.strip()
            if not token:
                continue
            if ":" not in token:
                raise ValueError(
                    f"Invalid agent specification '{token}'. Expected format agent:count"
                )
            agent_type, count_str = token.split(":", maxsplit=1)
            agent_type = agent_type.strip()
            try:
                count = int(count_str)
            except ValueError as exc:
                raise ValueError(
                    f"Instance count should be an integer for '{token}'"
                ) from exc

            if count < 1:
                raise ValueError(
                    f"Instance count must be >= 1 for agent '{agent_type}'"
                )

            base_config: AgentConfig = template.get(agent_type, {}).copy() if template else {}
            base_config["instances"] = count
            if task:
                base_config.setdefault("tasks", [task])
            agents[agent_type] = base_config

        if not agents:
            raise ValueError("No valid agent definitions found in specification")

        return cls(agents=agents)

    def merge(self, overrides: Dict[str, Any]) -> "SwarmConfig":
        """Return a new config with overrides applied."""

        merged_agents = _deep_update(self.agents, overrides.get("agents", {}))
        merged_deployment = _deep_update(self.deployment, overrides.get("deployment", {}))
        merged_metadata = _deep_update(self.metadata, overrides.get("metadata", {}))
        return SwarmConfig(
            agents=merged_agents,
            deployment=merged_deployment,
            metadata=merged_metadata,
        )

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agents": self.agents,
            "deployment": self.deployment,
            "metadata": self.metadata,
        }

    def to_yaml(self, file_path: str | Path) -> None:
        with Path(file_path).open("w", encoding="utf-8") as handle:
            yaml.safe_dump(self.to_dict(), handle, default_flow_style=False, sort_keys=False)

    def to_json(self, file_path: str | Path) -> None:
        with Path(file_path).open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2)

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------
    def validate(self) -> bool:
        if not self.agents:
            raise ValueError("Configuration must include at least one agent")

        for agent_type, config in self.agents.items():
            if not isinstance(config, dict):
                raise ValueError(
                    f"Agent '{agent_type}' configuration must be a dictionary"
                )

            instances = config.get("instances", 1)
            if not isinstance(instances, int) or instances < 1:
                raise ValueError(
                    f"Agent '{agent_type}' must declare at least one instance"
                )

        return True

    def get_total_instances(self) -> int:
        return sum(config.get("instances", 1) for config in self.agents.values())

    def get_agent_types(self) -> list[str]:
        return list(self.agents.keys())

    def iter_agents(self) -> Iterable[tuple[str, AgentConfig]]:
        return self.agents.items()


def create_default_config() -> SwarmConfig:
    """Create an opinionated default configuration."""

    return SwarmConfig(
        {
            "codex": {
                "instances": 1,
                "resources": {
                    "memory": "2GB",
                    "timeout": "30m",
                },
                "tasks": ["code_generation", "testing"],
            },
            "claude": {
                "instances": 1,
                "resources": {
                    "memory": "1GB",
                    "timeout": "30m",
                },
                "tasks": ["architecture_review", "documentation"],
            },
        }
    )


def create_example_config() -> str:
    """Return a YAML example configuration."""

    return """
agents:
  codex:
    instances: 3
    resources:
      memory: "2GB"
      timeout: "30m"
    tasks:
      - frontend_development
      - testing
  claude:
    instances: 2
    resources:
      memory: "1GB"
      timeout: "30m"
    tasks:
      - architecture_review
      - documentation
  gemini:
    instances: 1
    resources:
      memory: "1GB"
      timeout: "30m"
    tasks:
      - performance_analysis

deployment:
  strategy: parallel
  max_concurrent: 8
  monitoring:
    enabled: true
    dashboard_port: 8080
  logging:
    level: INFO
    format: json
metadata:
  created_by: agentswarm
  schema: v1
"""
