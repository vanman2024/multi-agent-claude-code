"""
Base Agent class - Abstract base for all agent implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import subprocess
import logging


@dataclass
class AgentProcess:
    """Represents a running agent process"""
    pid: int
    instance_id: int
    status: str
    memory_usage: Optional[str] = None
    uptime: Optional[str] = None


@dataclass
class AgentStatus:
    """Current status of an agent"""
    status: str  # "running", "stopped", "error", "starting"
    pid: Optional[int] = None
    memory_usage: Optional[str] = None
    uptime: Optional[str] = None
    last_activity: Optional[str] = None
    error_message: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all agent implementations"""
    
    def __init__(self, instance_id: int, config: Optional[Dict[str, Any]] = None):
        self.instance_id = instance_id
        self.config = config or {}
        self.process: Optional[subprocess.Popen] = None
        self.logger = logging.getLogger(f"{self.__class__.__name__}.{instance_id}")
    
    @abstractmethod
    async def deploy(self, task: str, config: Dict[str, Any]) -> AgentProcess:
        """Deploy agent with specific task"""
        pass
    
    @abstractmethod
    async def monitor(self) -> AgentStatus:
        """Get current agent status"""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the agent"""
        pass
    
    @abstractmethod
    async def restart(self) -> None:
        """Restart the agent"""
        pass
    
    def get_agent_type(self) -> str:
        """Get the agent type name"""
        return self.__class__.__name__.lower().replace('agent', '')
    
    def get_instance_id(self) -> int:
        """Get the instance ID"""
        return self.instance_id
    
    def is_running(self) -> bool:
        """Check if the agent process is running"""
        if self.process is None:
            return False
        return self.process.poll() is None
    
    def get_pid(self) -> Optional[int]:
        """Get process ID if running"""
        if self.process and self.is_running():
            return self.process.pid
        return None
    
    async def health_check(self) -> bool:
        """Basic health check - override for more sophisticated checks"""
        return self.is_running()
    
    def _build_command(self, task: str, config: Dict[str, Any]) -> str:
        """Build command to execute - override in subclasses"""
        return f"echo 'Base agent {self.instance_id}: {task}'"
    
    def _get_memory_usage(self) -> Optional[str]:
        """Get memory usage for the process"""
        try:
            if not self.is_running():
                return None
            
            import psutil
            process = psutil.Process(self.process.pid)
            memory_mb = process.memory_info().rss / 1024 / 1024
            return f"{memory_mb:.1f}MB"
        except Exception as e:
            self.logger.warning(f"Failed to get memory usage: {e}")
            return None
    
    def _get_uptime(self) -> Optional[str]:
        """Get uptime for the process"""
        try:
            if not self.is_running():
                return None
            
            import psutil
            process = psutil.Process(self.process.pid)
            create_time = process.create_time()
            uptime_seconds = psutil.time.time() - create_time
            
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception as e:
            self.logger.warning(f"Failed to get uptime: {e}")
            return None
    
    async def get_logs(self, lines: int = 100) -> str:
        """Get recent logs from the agent"""
        # TODO: Implement log retrieval
        return f"Logs for {self.get_agent_type()} instance {self.instance_id}"
    
    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration"""
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Update agent configuration"""
        self.config.update(new_config)
        self.logger.info(f"Updated configuration: {new_config}")