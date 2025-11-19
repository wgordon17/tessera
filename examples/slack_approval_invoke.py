#!/usr/bin/env python3
"""
Invoke SupervisorGraph with Slack approval workflow.

This script demonstrates invoking a LangGraph graph that will pause for
Slack approval when needed.

Prerequisites:
- Run slack_approval_demo.py in another terminal first
- That terminal must stay running to handle Slack events

Usage:
    export UV_PROJECT_ENVIRONMENT=.cache/.venv
    uv run python examples/slack_approval_invoke.py
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
    """Invoke graph with Slack approval."""
    print("🚀 Invoking SupervisorGraph with Slack Approval")
    print("=" * 60)

    # Check environment variables
    if not os.environ.get("SLACK_APPROVAL_CHANNEL"):
        print("❌ SLACK_APPROVAL_CHANNEL environment variable not set")
        return 1

    print("\n✅ Environment configured")
    print(f"   Channel: {os.environ['SLACK_APPROVAL_CHANNEL']}")

    # Initialize components
    print("\n🔧 Initializing components...")
    slack_client = create_slack_client()
    config = FrameworkConfig.from_env()
    supervisor = SupervisorGraph(config=config)
    coordinator = SlackApprovalCoordinator(graph=supervisor, slack_client=slack_client)
    print("   ✓ Ready")

    # Define task
    task = {
        "objective": "Build a web scraping system for product prices",
    }

    print(f"\n📋 Task: {task['objective']}")
    print("   Thread ID: demo-task-001")

    # Invoke with approval
    print("\n⏳ Invoking graph...")
    result = coordinator.invoke_with_slack_approval(
        input_data=task,
        thread_id="demo-task-001",
        slack_channel=os.environ["SLACK_APPROVAL_CHANNEL"],
    )

    # Check result
    print("\n" + "=" * 60)
    if "__interrupt__" in result:
        print("⏸️  PAUSED FOR APPROVAL")
        print()
        print("   The graph has been interrupted and is waiting for")
        print("   human approval in Slack.")
        print()
        print("   Check your Slack channel:")
        print(f"   {os.environ['SLACK_APPROVAL_CHANNEL']}")
        print()
        print("   Click 'Approve' or 'Reject' to continue.")
        print()
        interrupt_data = result["__interrupt__"]
        print(f"   Question: {interrupt_data.get('question', 'N/A')}")
        print(f"   Details: {interrupt_data.get('details', {})}")
    else:
        print("✅ COMPLETED")
        print()
        print("   Final result:")
        for key, value in result.items():
            if key.startswith("__"):
                continue
            print(f"   {key}: {value}")

    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
