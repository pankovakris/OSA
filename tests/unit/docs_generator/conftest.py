import pytest

from osa_tool.config.settings import ConfigLoader


@pytest.fixture(scope="session")
def config_loader():
    """
    Loads a pre-configured ConfigLoader instance for testing.

    This fixture sets up a ConfigLoader with predefined Git configuration
    values, including the project name, repository URL, host, and full name.

    Returns:
        ConfigLoader: A ConfigLoader instance configured for test purposes.
    """
    config_loader = ConfigLoader()
    config_loader.config.git.name = "TestProject"
    config_loader.config.git.repository = "https://github.com/user/TestProject"
    config_loader.config.git.host = "github"
    config_loader.config.git.full_name = "user/TestProject"
    return config_loader
