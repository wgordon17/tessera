"""
Multi-channel Slack client for agent communication.

Supports:
- Agent-to-agent collaboration channel
- Agent-to-user approval/question channel
- Agent identity management
- Threaded conversations
"""

import os
from typing import Optional, Dict, Any, List
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient

from .agent_identity import AgentIdentityManager, AgentIdentity


class MultiChannelSlackClient:
    """
    Multi-channel Slack client for Tessera.

    Manages communication across multiple channels with agent identities.
    """

    def __init__(
        self,
        bot_token: Optional[str] = None,
        app_token: Optional[str] = None,
        agent_channel: Optional[str] = None,
        user_channel: Optional[str] = None,
        identity_manager: Optional[AgentIdentityManager] = None,
    ):
        """
        Initialize multi-channel Slack client.

        Args:
            bot_token: Slack bot token (xoxb-...)
            app_token: Slack app token for Socket Mode (xapp-...)
            agent_channel: Channel ID for agent-to-agent communication
            user_channel: Channel ID for agent-to-user communication
            identity_manager: Optional custom identity manager
        """
        self.bot_token = bot_token or os.getenv("SLACK_BOT_TOKEN")
        self.app_token = app_token or os.getenv("SLACK_APP_TOKEN")
        self.agent_channel = agent_channel or os.getenv("SLACK_AGENT_CHANNEL")
        self.user_channel = user_channel or os.getenv("SLACK_USER_CHANNEL")

        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN required")

        self.web_client = WebClient(token=self.bot_token)
        self.socket_client = None
        if self.app_token:
            self.socket_client = SocketModeClient(
                app_token=self.app_token, web_client=self.web_client
            )

        self.identity_manager = identity_manager or AgentIdentityManager()

    def post_agent_message(
        self,
        agent_name: str,
        message: str,
        channel: Optional[str] = None,
        thread_ts: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post message as an agent to agent collaboration channel.

        Args:
            agent_name: Name of the agent posting
            message: Message text
            channel: Optional channel override (uses agent_channel by default)
            thread_ts: Optional thread timestamp for replies

        Returns:
            Slack API response
        """
        identity = self.identity_manager.get_identity(agent_name)
        channel = channel or self.agent_channel

        if not channel:
            raise ValueError("Agent channel not configured")

        response = self.web_client.chat_postMessage(
            channel=channel,
            text=message,
            username=identity.display_name,
            icon_emoji=identity.emoji,
            thread_ts=thread_ts,
            blocks=[
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*{identity.display_name}* • {identity.description}",
                        }
                    ],
                },
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
            ],
        )

        return response

    def post_user_request(
        self,
        agent_name: str,
        message: str,
        request_type: str = "approval",
        metadata: Optional[Dict[str, Any]] = None,
        channel: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Post approval/question request to user channel.

        Args:
            agent_name: Agent requesting approval
            message: Request message
            request_type: Type of request (approval, question, permission)
            metadata: Additional context
            channel: Optional channel override

        Returns:
            Slack API response with message timestamp
        """
        identity = self.identity_manager.get_identity(agent_name)
        channel = channel or self.user_channel

        if not channel:
            raise ValueError("User channel not configured")

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{identity.emoji} Agent {request_type.title()} Required",
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"From: *{identity.display_name}*",
                    }
                ],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        ]

        # Add metadata if provided
        if metadata:
            metadata_text = "\n".join(
                f"*{k.replace('_', ' ').title()}:* {v}" for k, v in metadata.items()
            )
            blocks.append(
                {"type": "section", "text": {"type": "mrkdwn", "text": metadata_text}}
            )

        # Add approval buttons for approval requests
        if request_type == "approval":
            blocks.append(
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Approve"},
                            "style": "primary",
                            "value": "approve",
                            "action_id": "approve_action",
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Deny"},
                            "style": "danger",
                            "value": "deny",
                            "action_id": "deny_action",
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Ask Question"},
                            "value": "question",
                            "action_id": "question_action",
                        },
                    ],
                }
            )

        response = self.web_client.chat_postMessage(
            channel=channel, text=message, blocks=blocks
        )

        return response

    def post_status_update(
        self, agent_name: str, status: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Post status update to agent channel.

        Args:
            agent_name: Agent name
            status: Status message (e.g., "Task completed", "In progress")
            details: Optional status details
        """
        message = f"*Status:* {status}"
        if details:
            message += "\n" + "\n".join(f"• {k}: {v}" for k, v in details.items())

        self.post_agent_message(agent_name, message)
