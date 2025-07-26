import os

import tomli

from osa_tool.utils import osa_project_root


class PromptLoader:
    """
    Loads prompts from a file.

    This class is designed to load prompts from a TOML file, providing a
    centralized location for managing and accessing prompt templates. It handles
    file loading and basic validation of the loaded prompts.

    Attributes:
    - prompts: A dictionary containing the loaded prompts.

    Class Methods:
    - __init__:
    """

    def __init__(self):
        """
        Initializes the PromptManager with loaded prompts.
        """
        self.prompts = self.load_prompts()

    def load_prompts(self) -> dict:
        """
        Load and validate prompts from prompts.toml file.
        """
        with open(self._get_prompts_path(), "rb") as file:
            prompts = tomli.load(file)

        return prompts.get("prompts", {})

    @staticmethod
    def _get_prompts_path() -> str:
        """
        Helper method to get the correct resource path.
        """
        file_path = os.path.join(
            osa_project_root(), "config", "settings", "prompts.toml"
        )
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompts file {file_path} not found.")
        return str(file_path)
