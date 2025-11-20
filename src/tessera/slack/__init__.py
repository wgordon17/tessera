"""
Enhanced Slack integration for Tessera.

Multi-channel agent communication and collaboration.
"""

from .multi_channel import MultiChannelSlackClient
from .agent_identity import AgentIdentityManager
from .approval import SlackApprovalCoordinator

__all__ = [
    "MultiChannelSlackClient",
    "AgentIdentityManager",
    "SlackApprovalCoordinator",
]
