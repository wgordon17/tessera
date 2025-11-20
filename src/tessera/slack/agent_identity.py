"""
Agent identity management for Slack.

Ensures each agent has a unique identity (username, icon, color) when
posting to Slack, while using a shared bot token.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class AgentIdentity:
    """Identity configuration for an agent in Slack."""

    name: str
    display_name: str  # "Tessera: Python Expert"
    emoji: str  # ":snake:"
    color: str  # "#4ECDC4" (for message attachments)
    description: str  # "Python coding specialist"


class AgentIdentityManager:
    """
    Manages agent identities for Slack messages.

    Each agent gets a unique persona while sharing the same bot token.
    """

    # Default identities for common agent types
    DEFAULT_IDENTITIES = {
        "supervisor": AgentIdentity(
            name="supervisor",
            display_name="Tessera: Supervisor",
            emoji=":construction_worker:",
            color="#FF6B6B",
            description="Task coordinator and orchestrator",
        ),
        "python-expert": AgentIdentity(
            name="python-expert",
            display_name="Tessera: Python Expert",
            emoji=":snake:",
            color="#4ECDC4",
            description="Python coding specialist",
        ),
        "test-engineer": AgentIdentity(
            name="test-engineer",
            display_name="Tessera: Test Engineer",
            emoji=":test_tube:",
            color="#45B7D1",
            description="Testing and quality assurance",
        ),
        "code-reviewer": AgentIdentity(
            name="code-reviewer",
            display_name="Tessera: Code Reviewer",
            emoji=":mag:",
            color="#5F27CD",
            description="Code quality and best practices",
        ),
        "security-expert": AgentIdentity(
            name="security-expert",
            display_name="Tessera: Security",
            emoji=":shield:",
            color="#EE5A6F",
            description="Security auditing",
        ),
        "tech-writer": AgentIdentity(
            name="tech-writer",
            display_name="Tessera: Documentation",
            emoji=":memo:",
            color="#00D2D3",
            description="Technical documentation",
        ),
    }

    def __init__(self, custom_identities: Optional[Dict[str, AgentIdentity]] = None):
        """
        Initialize agent identity manager.

        Args:
            custom_identities: Optional custom agent identities to add/override
        """
        self.identities = self.DEFAULT_IDENTITIES.copy()
        if custom_identities:
            self.identities.update(custom_identities)

    def get_identity(self, agent_name: str) -> AgentIdentity:
        """
        Get identity for an agent.

        Args:
            agent_name: Agent name

        Returns:
            AgentIdentity for the agent, or a default if not found
        """
        if agent_name in self.identities:
            return self.identities[agent_name]

        # Create default identity for unknown agents
        return AgentIdentity(
            name=agent_name,
            display_name=f"Tessera: {agent_name.replace('-', ' ').title()}",
            emoji=":robot_face:",
            color="#95A5A6",
            description=f"Agent: {agent_name}",
        )

    def register_identity(self, identity: AgentIdentity) -> None:
        """
        Register a new agent identity.

        Args:
            identity: AgentIdentity to register
        """
        self.identities[identity.name] = identity

    def format_message_header(self, agent_name: str) -> str:
        """
        Format message header with agent identity.

        Args:
            agent_name: Agent name

        Returns:
            Formatted header string for Slack message
        """
        identity = self.get_identity(agent_name)
        return f"{identity.emoji} *{identity.display_name}*\n_{identity.description}_"
