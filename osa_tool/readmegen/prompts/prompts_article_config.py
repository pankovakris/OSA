import os

import tomli

from osa_tool.utils import osa_project_root


class PromptArticleLoader:
    """
    Loads articles from prompts using a prompt template.

    This class is designed to load article content based on a given prompt,
    utilizing a pre-defined template for structuring the output. It's particularly
    useful when you need to generate articles or similar text formats programmatically.
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
        Helper method to get the correct resource path,
        looking outside the package.
        """
        file_path = os.path.join(
            osa_project_root(), "config", "settings", "prompts_article.toml"
        )
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompts file {file_path} not found.")
        return str(file_path)
