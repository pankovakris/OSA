from unittest import mock

import pytest

from osa_tool.docs_generator.contributing import ContributingBuilder


@pytest.fixture
def builder(config_loader):
    """
    Creates a ContributingBuilder instance with mocked dependencies.

    This method sets up mocks for SourceRank and load_data_metadata to provide
    a controlled environment for testing or demonstration purposes. It configures
    the mocks to simulate the presence of documentation, READMEs, and tests, as well
    as providing default metadata for a project.

    Args:
        config_loader: The configuration loader object.

    Returns:
        ContributingBuilder: An instance of the ContributingBuilder class.

    """
    with (
        mock.patch("osa_tool.docs_generator.contributing.SourceRank") as MockSourceRank,
        mock.patch(
            "osa_tool.docs_generator.contributing.load_data_metadata"
        ) as mock_metadata,
    ):
        mock_rank = MockSourceRank.return_value
        mock_rank.docs_presence.return_value = True
        mock_rank.readme_presence.return_value = True
        mock_rank.tests_presence.return_value = True
        mock_rank.tree = "docs/CONTRIBUTING.md\nREADME.md\ntests/"

        mock_metadata.return_value = mock.Mock(
            default_branch="main", name="TestProject", homepage_url=None
        )

        return ContributingBuilder(config_loader)


@mock.patch("osa_tool.docs_generator.contributing.save_sections")
@mock.patch("osa_tool.docs_generator.contributing.logger")
@mock.patch("osa_tool.docs_generator.contributing.os.makedirs")
@mock.patch("osa_tool.docs_generator.contributing.remove_extra_blank_lines")
def test_build_contributing(
    mock_remove_blank_lines, mock_makedirs, mock_logger, mock_save, builder
):
    """
    Tests the build_contributing method.
    """
    # Arrange
    expected_content = "\n".join(
        [
            builder.introduction,
            builder.guide,
            builder.before_pr,
            builder.acknowledgements,
        ]
    )
    mock_remove_blank_lines.return_value = None
    # Act
    builder.build()
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.file_to_save)
    mock_makedirs.assert_called_once_with(builder.repo_path)
    mock_logger.info.assert_called_once_with(
        f"CONTRIBUTING.md successfully generated in folder {builder.repo_path}"
    )


def test_introduction_content(builder):
    """
    Tests the content of the introduction string.

    Args:
        builder: The builder object containing the introduction string and issues URL.

    Returns:
        None
        Asserts that specific strings are not present or are present in the introduction string.
    """
    # Act
    intro = builder.introduction
    # Assert
    assert "Thanks for creating a Pull Request" not in intro
    assert "TestProject" in intro
    assert builder.issues_url in intro


def test_guide_content(builder):
    """
    Tests the content of the generated guide.

    Args:
        builder: The builder object used to create the guide.

    Returns:
        None
        Asserts that "TestProject" is present in the guide and that the builder's URL path is also included.
    """
    # Act
    guide = builder.guide
    # Assert
    assert "TestProject" in guide
    assert builder.url_path in guide


def test_before_pr_content(builder):
    """
    Checks that the 'before_pr' content includes expected elements.

    Args:
        builder: The builder object containing project files and documentation.

    Returns:
        None

    """
    # Act
    before_pr = builder.before_pr
    # Assert
    assert "TestProject" in before_pr
    assert builder.documentation in before_pr
    assert builder.readme in before_pr
    assert builder.tests in before_pr


def test_documentation_link(builder):
    """
    Checks if the documentation link is valid.

    Args:
        builder: The builder object containing documentation information.

    Returns:
        None
        Asserts that either "docs/CONTRIBUTING.md" or "example.com" is present in the documentation links.
    """
    # Act
    docs = builder.documentation
    # Assert
    assert "docs/CONTRIBUTING.md" in docs or "example.com" in docs


def test_readme_link(builder):
    """
    Checks if the README file is present in the project.

    Args:
        builder: The builder object containing the readme information.

    Returns:
        None
        Asserts that "README.md" is in the readme string.
    """
    # Act
    readme = builder.readme
    # Assert
    assert "README.md" in readme


def test_tests_link(builder):
    """
    Tests that the tests link is correct.

    Args:
        builder: The builder object to test with.

    Returns:
        None
    """
    # Act
    tests = builder.tests
    # Assert
    assert "tests/" in tests


def test_acknowledgements_content(builder):
    """
    Tests the content of the acknowledgements string.

    Args:
        builder: The builder object containing the acknowledgements.

    Returns:
        None

    """
    # Act
    ack = builder.acknowledgements
    # Assert
    assert isinstance(ack, str)
    assert len(ack) > 0
