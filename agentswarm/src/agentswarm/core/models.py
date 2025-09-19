"""Shared data models for AgentSwarm core components."""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class AgentProcess:
    """Represents a running agent process."""

    pid: int
    agent_type: str
    instance_id: int
    command: str
    status: str = "running"
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None
    start_time: float = field(default_factory=time.time)
    handle: Optional[subprocess.Popen] = field(default=None, repr=False)

    def is_alive(self) -> bool:
        if self.handle is not None and self.handle.poll() is None:
            return True
        if self.pid <= 0:
            return False
        try:
            os.kill(self.pid, 0)
        except OSError:
            return False
        return True

    def terminate(self, *, graceful: bool = True) -> None:
        if self.handle is not None and self.handle.poll() is None:
            if graceful:
                self.handle.terminate()
            else:
                self.handle.kill()
        else:
            try:
                if graceful:
                    os.kill(self.pid, 15)
                else:
                    os.kill(self.pid, 9)
            except OSError:
                pass
        self.status = "terminated"


@dataclass(slots=True)
class SwarmDeployment:
    """Represents a deployed agent swarm."""

    agents: Dict[str, List[AgentProcess]]
    config: Any  # SwarmConfig, but avoid circular imports
    deployment_id: str
    start_time: str
