#!/usr/bin/env python3
"""
Demonstration of Slack Socket Mode Human-in-the-Loop integration with LangGraph.

This example shows how to use LangGraph's interrupt() function with Slack Socket Mode
for approval workflows without requiring webhook endpoints.

Setup required:
1. Create Slack app with Socket Mode enabled
2. Set environment variables:
   - SLACK_APP_TOKEN (xapp-...)
   - SLACK_BOT_TOKEN (xoxb-...)
   - SLACK_APPROVAL_CHANNEL (C...)
   - COPILOT_API_KEY or OPENAI_API_KEY

Usage:
    export UV_PROJECT_ENVIRONMENT=.cache/.venv
    export SLACK_APP_TOKEN=xapp-...
    export SLACK_BOT_TOKEN=xoxb-...
    export SLACK_APPROVAL_CHANNEL=C...
    uv run python examples/slack_approval_demo.py
"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from tessera.slack_approval import SlackApprovalCoordinator, create_slack_client
from tessera.supervisor_graph import SupervisorGraph
from tessera.config import FrameworkConfig


def main():
    """Run Slack Approval demo."""
    print("🤖 Slack Approval Demo - LangGraph + Socket Mode")
    print("=" * 60)

    # Check environment variables
    required_env_vars = [
        "SLACK_APP_TOKEN",
        "SLACK_BOT_TOKEN",
        "SLACK_APPROVAL_CHANNEL",
    ]

    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("\nSetup instructions:")
        print("1. Create a Slack app: https://api.slack.com/apps")
        print("2. Enable Socket Mode in app settings")
        print("3. Create app-level token with connections:write scope")
        print("4. Create bot token with chat:write scope")
        print("5. Set environment variables:")
        print("   export SLACK_APP_TOKEN=xapp-...")
        print("   export SLACK_BOT_TOKEN=xoxb-...")
        print("   export SLACK_APPROVAL_CHANNEL=C...")
        return 1

    print("\n✅ Environment variables configured")
    print(f"   Channel: {os.environ['SLACK_APPROVAL_CHANNEL']}")

    # Initialize Slack client
    print("\n🔌 Connecting to Slack via Socket Mode...")
    slack_client = create_slack_client()
    print("   ✓ Socket Mode client initialized")

    # Initialize supervisor graph
    print("\n📊 Initializing SupervisorGraph...")
    config = FrameworkConfig.from_env()
    supervisor = SupervisorGraph(config=config)
    print(f"   ✓ Using {config.llm.provider} / {config.llm.model}")

    # Initialize Approval coordinator
    print("\n🔗 Setting up Approval coordinator...")
    coordinator = SlackApprovalCoordinator(
        graph=supervisor, slack_client=slack_client
    )

    # Register event handler
    event_handler = coordinator.create_event_handler()
    slack_client.socket_mode_request_listeners.append(event_handler)
    print("   ✓ Event handler registered")

    # Connect to Slack
    print("\n📡 Connecting to Slack workspace...")
    print("   (This will keep running until you press Ctrl+C)")
    print()
    print("=" * 60)
    print("🎯 READY! Send a task to test the approval workflow:")
    print()
    print("  In another terminal:")
    print("  python -c '")
    print("  from tessera.slack_approval import create_slack_client")
    print("  from tessera.supervisor_graph import SupervisorGraph")
    print("  from tessera.slack_approval import SlackApprovalCoordinator")
    print()
    print("  slack_client = create_slack_client()")
    print("  supervisor = SupervisorGraph()")
    print("  coordinator = SlackApprovalCoordinator(supervisor, slack_client)")
    print()
    print("  result = coordinator.invoke_with_slack_approval(")
    print('      input_data={"objective": "Build a web scraping system"},')
    print('      thread_id="demo-123",')
    print('      slack_channel="' + os.environ['SLACK_APPROVAL_CHANNEL'] + '"')
    print("  )")
    print("  '")
    print()
    print("  Or check the examples/slack_approval_invoke.py script")
    print("=" * 60)
    print()

    try:
        # This blocks and handles events until interrupted
        slack_client.connect()
    except KeyboardInterrupt:
        print("\n\n👋 Disconnecting from Slack...")
        slack_client.close()
        print("   ✓ Disconnected")
        return 0


if __name__ == "__main__":
    sys.exit(main())
