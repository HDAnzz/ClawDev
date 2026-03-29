"""
Chat environment for ClawDev framework.

Manages the state and data throughout the software development process.
"""


class ChatEnv:
    """Environment that tracks the state of a software development project."""

    def __init__(self, project_name: str):
        """
        Initialize environment for a project.

        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.task_prompt = ""
        self.modality = ""
        self.language = ""
