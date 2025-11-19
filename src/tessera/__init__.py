"""
Autonomy: Multi-agent AI framework with Supervisor and Interviewer personas.
"""

from .supervisor import SupervisorAgent
from .interviewer import InterviewerAgent
from .panel import PanelSystem
from .models import Task, AgentResponse, InterviewResult, PanelResult
from .copilot_proxy import CopilotProxyManager, start_proxy, stop_proxy, is_proxy_running

__version__ = "0.1.0"

__all__ = [
    "SupervisorAgent",
    "InterviewerAgent",
    "PanelSystem",
    "Task",
    "AgentResponse",
    "InterviewResult",
    "PanelResult",
    "CopilotProxyManager",
    "start_proxy",
    "stop_proxy",
    "is_proxy_running",
]
