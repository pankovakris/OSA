from unittest.mock import Mock, patch

import pytest

from osa_tool.aboutgen.about_generator import AboutGenerator


def test_init(about_generator, mock_config_loader):
    """
    Tests the initialization of the AboutGenerator class.

    Args:
        about_generator: The AboutGenerator instance to test.
        mock_config_loader: A mock config loader object.

    Returns:
        None
    """
    assert about_generator.config == mock_config_loader.config
    assert about_generator.repo_url == "https://github.com/test/repo"
    assert about_generator._content is None


def test_generate_about_content(about_generator, mocker):
    """
    Tests the generate_about_content method.

    This test mocks the underlying methods for generating description,
    detecting homepage, and generating topics to ensure that the
    generate_about_content method correctly combines their results into
    the _content attribute.

    Args:
        about_generator: The instance of the AboutGenerator class being tested.
        mocker: The pytest mocker object used for patching.

    Returns:
        None
    """
    mock_desc = "Test description"
    mock_homepage = "https://test.com"
    mock_topics = ["test", "python"]

    mocker.patch.object(about_generator, "generate_description", return_value=mock_desc)
    mocker.patch.object(about_generator, "detect_homepage", return_value=mock_homepage)
    mocker.patch.object(about_generator, "generate_topics", return_value=mock_topics)

    about_generator.generate_about_content()

    assert about_generator._content == {
        "description": mock_desc,
        "homepage": mock_homepage,
        "topics": mock_topics,
    }


def test_generate_description_from_metadata(about_generator, mock_metadata):
    """
    Tests generate_description() uses existing description from metadata.

    Args:
        about_generator: The AboutGenerator instance to test with.
        mock_metadata: A mock Metadata object with a description attribute.

    Returns:
        None.  The method asserts that the generated description matches the
        existing description in the metadata.
    """
    mock_metadata.description = "Existing description"
    about_generator.metadata = mock_metadata

    result = about_generator.generate_description()
    assert result == "Existing description"


def test_generate_description_from_readme(
    about_generator, sample_readme_content, mocker
):
    """
    Tests generating a description from the README content.

    Args:
        about_generator: The AboutGenerator instance to test with.
        sample_readme_content: The content of the sample README file.
        mocker: The mocker fixture for mocking dependencies.

    Returns:
        The generated description as returned by the model handler's send_request method.
    """
    about_generator.metadata = mocker.Mock()
    about_generator.metadata.description = None

    about_generator.readme_content = sample_readme_content

    mock_response = "Generated description"
    mocker.patch.object(
        about_generator.model_handler, "send_request", return_value=mock_response
    )

    result = about_generator.generate_description()

    assert result == mock_response
    about_generator.model_handler.send_request.assert_called_once()


def test_generate_topics_with_existing(about_generator, mock_metadata):
    """
    Tests generate_topics with existing topics.
    """
    mock_metadata.topics = ["python", "testing"]
    about_generator.metadata = mock_metadata

    result = about_generator.generate_topics(amount=2)
    assert result == ["python", "testing"]


def test_generate_topics_new(about_generator, mocker):
    """
    Tests the generate_topics_new method.

    Args:
        about_generator: The about generator object to be tested.
        mocker: The mocker object for patching and mocking.

    Returns:
        None

    """
    about_generator.metadata = mocker.Mock()
    about_generator.metadata.topics = []
    mock_response = "python,testing,automation"

    mocker.patch.object(
        about_generator.model_handler, "send_request", return_value=mock_response
    )
    mocker.patch.object(
        about_generator, "_validate_github_topics", return_value=["python", "testing"]
    )
    result = about_generator.generate_topics()

    assert set(result) == {"python", "testing"}
    about_generator.model_handler.send_request.assert_called_once()
    about_generator._validate_github_topics.assert_called_once_with(
        ["python", "testing", "automation"]
    )


def test_detect_homepage_from_metadata(about_generator, mock_metadata):
    """
    Detects the homepage URL from metadata.

    Args:
        about_generator: The AboutGenerator instance.
        mock_metadata: A mock metadata object with a homepage URL.

    Returns:
        str: The detected homepage URL.

    """
    mock_metadata.homepage_url = "https://test.com"
    about_generator.metadata = mock_metadata

    result = about_generator.detect_homepage()
    assert result == "https://test.com"


def test_detect_homepage_from_readme(about_generator, sample_readme_content, mocker):
    """
    Detects the homepage URL from the README content.

    Args:
        about_generator: The AboutGenerator instance to use.
        sample_readme_content: The content of the README file.
        mocker: The mocker object for patching.

    Returns:
        str: The detected homepage URL.

    """
    about_generator.readme_content = sample_readme_content
    about_generator.metadata.homepage_url = None

    urls = ["https://docs.test-project.com", "https://test-project.com"]
    mocker.patch.object(about_generator, "_extract_readme_urls", return_value=urls)
    mocker.patch.object(about_generator, "_analyze_urls", return_value=urls)

    result = about_generator.detect_homepage()
    assert result == "https://docs.test-project.com"


def test_extract_readme_urls(about_generator, sample_readme_content):
    """
    Tests the extraction of URLs from README content.

    Args:
        about_generator: The AboutGenerator instance being tested.
        sample_readme_content: The string content of a sample README file.

    Returns:
        None

    """
    result = about_generator._extract_readme_urls(sample_readme_content)
    expected = ["https://docs.test-project.com", "https://test-project.com"]
    assert set(result) == set(expected)


def test_get_about_section_message(about_generator):
    """
    Tests the generation of the about section message.

    Args:
        about_generator: The AboutSectionGenerator instance to test with.

    Returns:
        None
    """
    content = {
        "description": "Test description",
        "homepage": "https://test.com",
        "topics": ["python", "testing"],
    }
    about_generator._content = content

    message = about_generator.get_about_section_message()
    assert "Test description" in message
    assert "https://test.com" in message
    assert "`python`" in message
    assert "`testing`" in message
