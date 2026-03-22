"""
Main entry point for ClawDev framework.

This script provides a command-line interface to run the ClawDev framework
with different configurations and options.
"""

import argparse
import logging
import sys
import os
import json
from dotenv import load_dotenv

# Add src to path so we can import clawdev
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from clawdev.chain.chain import ChatChain
from clawdev.adapter.agent_adapter import AgentAdapter
from openclaw_acp import OpenClawAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("openclaw_acp.agent")


def main():
    """Main function to run the ClawDev framework."""
    parser = argparse.ArgumentParser(
        description="ClawDev - Multi-agent software development framework"
    )
    parser.add_argument("task", help="The development task to execute")
    parser.add_argument(
        "--project-name",
        "-p",
        default="clawdev_project",
        help="Name of the project directory",
    )
    parser.add_argument(
        "--config", "-c", default="default", help="Configuration to use"
    )

    args = parser.parse_args()

    print("Starting ClawDev framework...")
    print(f"Task: {args.task}")
    print(f"Project name: {args.project_name}")
    print(f"Configuration: {args.config}")

    # Run with real OpenClaw agents
    print("Connecting to OpenClaw agents...")
    agent_configs = {
        "Chief Executive Officer": "chief_executive_officer",
        "Chief Product Officer": "chief_product_officer",
        "Chief Technology Officer": "chief_technology_officer",
        "Programmer": "programmer",
        "Code Reviewer": "code_reviewer",
        "Software Test Engineer": "software_test_engineer",
        "Chief Creative Officer": "chief_creative_officer",
        "Counselor": "counselor",
        "Chief Human Resource Officer": "chief_human_resource_officer",
    }
    adapter = AgentAdapter(agent_configs)

    # Create a ChatChain with the adapter
    chain = ChatChain(adapter, config_name=args.config)

    # Run the development chain
    try:
        chain.run(args.task, args.project_name)
        print(
            f"Development process completed! Project created in projects/{args.project_name}"
        )
    except Exception as e:
        print(f"Error during development process: {e}")
        return 1
    finally:
        try:
            adapter.reset()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
