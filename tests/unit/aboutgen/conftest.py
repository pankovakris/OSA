from unittest.mock import Mock

import pytest

from osa_tool.aboutgen.about_generator import AboutGenerator
from osa_tool.analytics.metadata import RepositoryMetadata
from osa_tool.config.settings import ConfigLoader


@pytest.fixture
def mock_config():
    """
    Creates a mock configuration object for testing.

    Args:
        None

    Returns:
        Mock: A Mock object configured with a sample Git repository URL.
    """
    config = Mock()
    config.git.repository = "https://github.com/test/repo"
    return config


@pytest.fixture
def mock_config_loader(mock_config):
    """
    Creates a mock ConfigLoader instance.

    Args:
        mock_config: The configuration object to be used by the loader.

    Returns:
        A Mock ConfigLoader instance with the specified configuration.
    """
    loader = Mock(spec=ConfigLoader)
    loader.config = mock_config
    return loader


@pytest.fixture
def mock_metadata():
    """
    Creates a mock RepositoryMetadata object with default values.

    This method is useful for testing purposes when a real
    RepositoryMetadata object is not needed or available.

    Args:
        None

    Returns:
        Mock: A Mock object configured to resemble RepositoryMetadata,
              with description and homepage_url set to None, topics as an empty list,
              and default_branch set to "main".
    """
    metadata = Mock(spec=RepositoryMetadata)
    metadata.description = None
    metadata.homepage_url = None
    metadata.topics = []
    metadata.default_branch = "main"
    return metadata


@pytest.fixture
def sample_readme_content():
    """
    Returns a sample README content string.

    This method provides a pre-defined string that can be used as
    a placeholder or example for a project's README file. It includes
    headings, descriptions, and links to documentation and homepage.

    Args:
        None

    Returns:
        str: A formatted string representing the sample README content.
    """
    return """
    # Test Project
    
    This is a test project that does amazing things.
    Check out our [documentation](https://docs.test-project.com).
    Visit our [homepage](https://test-project.com).
    """


@pytest.fixture
def about_generator(mock_config_loader, mocker):
    """
    Creates an instance of the AboutGenerator class with mocked dependencies.

    Args:
        mock_config_loader: A mock object for loading configuration data.
        mocker: A mocker object used for patching dependencies.

    Returns:
        AboutGenerator: An instance of the AboutGenerator class.
    """
    mocker.patch("osa_tool.aboutgen.about_generator.load_data_metadata")
    mocker.patch("osa_tool.aboutgen.about_generator.extract_readme_content")
    mocker.patch("osa_tool.aboutgen.about_generator.ModelHandlerFactory.build")
    return AboutGenerator(mock_config_loader)
