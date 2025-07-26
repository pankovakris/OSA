import os
import re

from osa_tool.config.settings import ConfigLoader
from osa_tool.utils import get_repo_tree, parse_folder_name


class SourceRank:
    """
    Calculates a source rank for open-source repositories based on various factors.

    This class analyzes a repository to determine the presence of key elements
    like README, license, examples, documentation, tests, citation information, and
    contributing guidelines, contributing to an overall 'source rank'.
    """

    def __init__(self, config_loader: ConfigLoader):
        """
        self.config = config_loader.config
                self.repo_url = self.config.git.repository
                self.repo_path = os.path.join(os.getcwd(), parse_folder_name(self.repo_url))
                self.tree = get_repo_tree(self.repo_path)
        """
        self.config = config_loader.config
        self.repo_url = self.config.git.repository
        self.repo_path = os.path.join(os.getcwd(), parse_folder_name(self.repo_url))
        self.tree = get_repo_tree(self.repo_path)

    def readme_presence(self) -> bool:
        """
        No valid docstring found.
        """
        pattern = re.compile(r"\bREADME(\.\w+)?\b", re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def license_presence(self) -> bool:
        """
        No valid docstring found.
        """
        pattern = re.compile(r"\bLICEN[SC]E(\.\w+)?\b", re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def examples_presence(self) -> bool:
        """
        Checks if the repository contains an 'examples' directory.

        Args:
            None

        Returns:
            bool: True if a directory named 'examples', 'example',
                'tutorials', or 'tutorial' (case-insensitive) is present in the
                repository tree, False otherwise.

        """
        pattern = re.compile(r"\b(tutorials?|examples|notebooks?)\b", re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def docs_presence(self) -> bool:
        """
        Checks if the repository contains documentation related keywords.

        Args:
            None

        Returns:
            bool: True if documentation-related keywords are found, False otherwise.

        """
        pattern = re.compile(r"\b(docs?|documentation|wiki|manuals?)\b", re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def tests_presence(self) -> bool:
        """
        No valid docstring found.
        """
        pattern = re.compile(
            r"\b(tests?|testcases?|unittest|test_suite)\b", re.IGNORECASE
        )
        return bool(pattern.search(self.tree))

    def citation_presence(self) -> bool:
        """
        Checks if a CITATION file or reference to one exists in the repository.

        Args:
            None

        Returns:
            bool: True if a CITATION file or reference is found, False otherwise.

        """
        pattern = re.compile(r"\bCITATION(\.\w+)?\b", re.IGNORECASE)
        return bool(pattern.search(self.tree))

    def contributing_presence(self) -> bool:
        """
        Checks if a contributing guide exists in the repository.

        Args:
            self: The repository object containing the file tree.

        Returns:
            bool: True if a contributing guide is found, False otherwise.
        """
        pattern = re.compile(r"\b\w*contribut\w*\.(md|rst|txt)$", re.IGNORECASE)
        return bool(pattern.search(self.tree))
