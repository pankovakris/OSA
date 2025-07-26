import pytest


@pytest.mark.parametrize(
    "tree, expected",
    [("README.md", True), ("readme.txt", True), ("docs/guide.pdf", False)],
)
def test_readme_presence(source_rank, tree, expected):
    """
    Checks if a README file exists in the given tree.

    Args:
        source_rank: The source rank object (used for accessing the tree).
        tree: The path to the root of the repository tree.
        expected: The expected boolean value indicating whether a README should be present.

    Returns:
        None
    """
    # Arrange
    source_rank.tree = tree
    # Act
    assert source_rank.readme_presence() == expected


@pytest.mark.parametrize(
    "tree, expected", [("LICENSE", True), ("Licence.txt", True), ("README.md", False)]
)
def test_license_presence(source_rank, tree, expected):
    """
    Checks if a license file is present in the given tree.

    Args:
        source_rank: The source rank object (used for accessing the tree).
        tree: The name of the directory/file to check within the repository.
        expected: The expected boolean value indicating whether a license should be found.

    Returns:
        bool: True if a license file is present, False otherwise.
    """
    # Arrange
    source_rank.tree = tree
    # Assert
    assert source_rank.license_presence() == expected


@pytest.mark.parametrize(
    "tree, expected",
    [("examples/", True), ("notebook.ipynb", True), ("source_code.py", False)],
)
def test_examples_presence(source_rank, tree, expected):
    """
    Tests the presence of examples within a given tree structure.

    Args:
        source_rank: The source rank object used for testing.
        tree: The path to the tree or file being tested.
        expected: The expected boolean value indicating whether examples should be present.

    Returns:
        None
    """
    # Arrange
    source_rank.tree = tree
    # Assert
    assert source_rank.examples_presence() == expected


@pytest.mark.parametrize(
    "tree, expected",
    [("docs/", True), ("documentation/index.html", True), ("source_code.py", False)],
)
def test_docs_presence(source_rank, tree, expected):
    """
    Checks if documentation exists at the given tree path.

    Args:
        source_rank: The source rank object (used for accessing the tree).
        tree: The path to check for documentation.
        expected: The expected boolean value indicating whether docs should be present.

    Returns:
        bool: True if documentation is present at the given path, False otherwise.
    """
    # Arrange
    source_rank.tree = tree
    # Assert
    assert source_rank.docs_presence() == expected


@pytest.mark.parametrize(
    "tree, expected", [("tests/", True), ("unittest/", True), ("code/main.py", False)]
)
def test_tests_presence(source_rank, tree, expected):
    """
    Tests the presence of tests in a given tree.

    Args:
        source_rank: The source rank object (used for setting the tree).
        tree: The path to the tree to check.
        expected: The expected boolean value indicating whether tests should be present.

    Returns:
        None. Asserts that the `tests_presence()` method of the `source_rank` object returns the expected value.
    """
    # Arrange
    source_rank.tree = tree
    # Assert
    assert source_rank.tests_presence() == expected
