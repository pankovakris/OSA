import pytest
import nbformat
from unittest.mock import patch, mock_open

from osa_tool.convertion.notebook_converter import NotebookConverter


@pytest.fixture
def converter():
    """
    Creates a NotebookConverter object.

    Args:
        None

    Returns:
        NotebookConverter: An instance of the NotebookConverter class.
    """
    return NotebookConverter()


def create_test_notebook():
    """
    Creates a test Jupyter Notebook.

    Args:
        None

    Returns:
        nbformat.v4.Notebook: A new Jupyter Notebook object with example code
            for plotting and displaying a Pandas DataFrame.

    """
    nb = nbformat.v4.new_notebook()
    nb.cells.append(
        nbformat.v4.new_code_cell(
            """
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df.head()

plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
"""
        )
    )
    return nb


@pytest.fixture
def tmp_notebook(tmp_path):
    """
    Creates a temporary notebook file.

    Args:
        tmp_path: The path to the temporary directory.

    Returns:
        str: The path to the created notebook file.

    """
    nb = create_test_notebook()
    notebook_path = tmp_path / "test_notebook.ipynb"
    with open(notebook_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    return notebook_path


@patch.object(NotebookConverter, "convert_notebooks_in_directory")
def test_process_path_with_directory(mock_convert, tmpdir, converter):
    """
    Tests processing a path that points to a directory.

    Args:
        mock_convert: A mock object for the convert_notebooks_in_directory method.
        tmpdir: A temporary directory fixture.
        converter: The NotebookConverter instance being tested.

    Returns:
        None

    """
    # Arrange
    test_dir = tmpdir.mkdir("test_dir")
    test_file = test_dir.join("test.ipynb")
    test_file.write("content")
    # Act
    converter.process_path(str(test_dir))
    # Assert
    mock_convert.assert_called_once_with(str(test_dir))


@patch.object(NotebookConverter, "convert_notebook")
def test_process_path_with_file(mock_convert, tmpdir, converter):
    """
    Tests processing a path with an existing notebook file.

    Args:
        mock_convert: A mock object for the NotebookConverter's convert_notebook method.
        tmpdir: A temporary directory to create test files in.
        converter: An instance of the NotebookConverter class.

    Returns:
        None
    """
    # Arrange
    test_file = tmpdir.join("test.ipynb")
    test_file.write("content")
    # Act
    converter.process_path(str(test_file))
    # Assert
    mock_convert.assert_called_once_with(str(test_file))


def test_convert_notebook_success(tmp_notebook):
    """
    Tests successful conversion of a notebook to a Python script.

    Args:
        tmp_notebook: A temporary notebook file path.

    Returns:
        None

    """
    # Arrange
    converter = NotebookConverter()
    converter.convert_notebook(str(tmp_notebook))

    script_path = tmp_notebook.with_suffix(".py")
    # Act
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()
    # Assert
    assert script_path.exists()
    assert "plt.show()" not in script_content
    assert "plt.savefig(" in script_content
    assert ".head()" not in script_content


@patch("logging.Logger.error")
def test_convert_notebook_invalid(mock_logger):
    """
    Tests the convert_notebook method with an invalid notebook file.

    Args:
        mock_logger: A mock logger object to capture error messages.

    Returns:
        None
    """
    # Arrange
    converter = NotebookConverter()
    # Act
    with patch("builtins.open", mock_open(read_data="invalid")):
        converter.convert_notebook("invalid.ipynb")
        # Assert
        mock_logger.assert_called_with(
            "Failed to convert notebook %s: %s",
            "invalid.ipynb",
            mock_logger.call_args[0][2],
        )


@pytest.mark.parametrize(
    "input_code,expected",
    [
        (
            "plt.show()",
            "import os\nos.makedirs('test_figures', exist_ok=True)\nplt.savefig(os.path.join('test_figures', f'figure_line3.png'))\nplt.close()\n",
        ),
        (
            "    plt.show()",
            "import os\nos.makedirs('test_figures', exist_ok=True)\n    plt.savefig(os.path.join('test_figures', f'figure_line3.png'))\n    plt.close()\n",
        ),
    ],
)
def test_process_visualizations(converter, input_code, expected):
    """
    Tests the process_visualizations method with various input codes.

    Args:
        converter: The converter object used for processing visualizations.
        input_code: The input code string containing visualization commands.
        expected: The expected processed code string.

    Returns:
        None
    """
    # Act
    processed = converter.process_visualizations("test", input_code)
    # Assert
    assert processed.strip() == expected.strip()


def test_syntax_check_valid(converter):
    """
    Checks if the syntax check identifies valid Python code correctly.

    Args:
        converter: The converter object being tested.

    Returns:
        None
    """
    # Assert
    assert converter.is_syntax_correct("print('Hello World')") is True


def test_syntax_check_invalid(converter):
    """
    Tests that the syntax check returns False for invalid Python code.

    Args:
        converter: The converter object being tested.

    Returns:
        None
    """
    # Assert
    assert converter.is_syntax_correct("print('Hello World'") is False
