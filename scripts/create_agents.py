"""
Script to create all required OpenClaw agents for the ClawDev framework.
"""

import sys
import subprocess
import os


def create_agent(agent_name):
    """Create an OpenClaw agent with the given name."""
    print(f"Creating agent: {agent_name}")
    try:
        # Create workspace directory
        workspace_dir = f"/home/anzz/.openclaw/workspace-{agent_name.lower()}"
        os.makedirs(workspace_dir, exist_ok=True)

        # Use openclaw agents add command to create the agent in non-interactive mode
        subprocess.run(
            [
                "openclaw",
                "agents",
                "add",
                agent_name,
                "--non-interactive",
                "--workspace",
                workspace_dir,
            ],
            capture_output=True,
            text=True,
            cwd="/app/ClawDev",
            check=True,  # This will raise CalledProcessError if the command fails
        )
        print(f"Successfully created agent: {agent_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create agent {agent_name}: {e.stderr}")
        return False
    except Exception as e:
        print(f"Failed to create agent {agent_name}: {e}")
        return False


def main():
    """Main function to create all required agents."""
    # List of agents to create based on RoleConfig.json
    # Each role gets its own unique agent name to avoid confusion
    agents = [
        "Chief_Executive_Officer",
        "Chief_Product_Officer",
        "Chief_Technology_Officer",
        "Programmer",
        "Code_Reviewer",
        "Software_Test_Engineer",
        "Chief_Creative_Officer",
        "Counselor",
        "Chief_Human_Resource_Officer",
    ]

    print("Creating OpenClaw agents for ClawDev framework...")

    success_count = 0
    for agent_name in agents:
        if create_agent(agent_name):
            success_count += 1

    print(f"\nCreated {success_count}/{len(agents)} agents successfully.")

    if success_count == len(agents):
        print("All agents created successfully!")
        return 0
    else:
        print("Some agents failed to create.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
