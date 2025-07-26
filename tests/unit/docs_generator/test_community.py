from unittest import mock

import pytest

from osa_tool.docs_generator.community import CommunityTemplateBuilder


@pytest.fixture
def builder(config_loader):
    """
    Builds a CommunityTemplateBuilder instance with mocked dependencies.

    Args:
        config_loader: The config loader object used by the builder.

    Returns:
        CommunityTemplateBuilder: An instance of CommunityTemplateBuilder.

    """
    with (
        mock.patch("osa_tool.docs_generator.community.SourceRank") as MockSourceRank,
        mock.patch(
            "osa_tool.docs_generator.community.load_data_metadata"
        ) as mock_metadata,
    ):
        mock_rank = MockSourceRank.return_value
        mock_rank.contributing_presence.return_value = True
        mock_rank.docs_presence.return_value = True
        mock_rank.tree = ["docs/CONTRIBUTING.md"]

        mock_metadata.return_value = mock.Mock(
            default_branch="main", name="TestProject"
        )

        return CommunityTemplateBuilder(config_loader)


@mock.patch("osa_tool.docs_generator.community.save_sections")
@mock.patch("osa_tool.docs_generator.community.logger")
def test_build_code_of_conduct(mock_logger, mock_save, builder):
    """
    Tests building the code of conduct section.
    """
    # Act
    builder.build_code_of_conduct()
    expected_content = builder._template["code_of_conduct"]
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.code_of_conduct_to_save)
    mock_logger.info.assert_called_once()


@mock.patch("osa_tool.docs_generator.community.save_sections")
@mock.patch("osa_tool.docs_generator.community.logger")
@mock.patch(
    "osa_tool.docs_generator.community.find_in_repo_tree",
    return_value="docs/CONTRIBUTING.md",
)
def test_build_pull_request(mock_find, mock_logger, mock_save, builder):
    """
    Builds a pull request and asserts that the correct content is saved.

    Args:
        mock_find: Mock for find_in_repo_tree function.
        mock_logger: Mock for logger object.
        mock_save: Mock for save_sections function.
        builder: The builder object to test.

    Returns:
        None

    """
    # Act
    builder.build_pull_request()
    contributing_url = (
        f"https://github.com/user/TestProject/tree/main/docs/CONTRIBUTING.md"
    )
    expected_content = builder._template["pull_request"].format(
        contributing_url=contributing_url
    )
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.pr_to_save)
    mock_logger.info.assert_called_once()


@mock.patch("osa_tool.docs_generator.community.save_sections")
@mock.patch("osa_tool.docs_generator.community.logger")
def test_build_documentation_issue(mock_logger, mock_save, builder):
    """
    Tests building documentation for a single issue.

    Args:
        mock_logger: Mock logger object.
        mock_save: Mock save function.
        builder: The builder instance used to build the documentation.

    Returns:
        None
    """
    # Act
    builder.build_documentation_issue()
    expected_content = builder._template["docs_issue"]
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.docs_issue_to_save)
    mock_logger.info.assert_called_once()


@mock.patch("osa_tool.docs_generator.community.save_sections")
@mock.patch("osa_tool.docs_generator.community.logger")
def test_build_feature_issue(mock_logger, mock_save, builder):
    """
    Tests building a feature issue.
    """
    # Act
    builder.build_feature_issue()
    expected_content = builder._template["feature_issue"].format(
        project_name=builder.metadata.name
    )
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.feature_issue_to_save)
    mock_logger.info.assert_called_once()


@mock.patch("osa_tool.docs_generator.community.save_sections")
@mock.patch("osa_tool.docs_generator.community.logger")
def test_build_bug_issue(mock_logger, mock_save, builder):
    """
    Tests building a bug issue.
    """
    # Act
    builder.build_bug_issue()
    expected_content = builder._template["bug_issue"].format(
        project_name=builder.metadata.name
    )
    # Assert
    mock_save.assert_called_once_with(expected_content, builder.bug_issue_to_save)
    mock_logger.info.assert_called_once()
