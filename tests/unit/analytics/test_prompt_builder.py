from osa_tool.analytics.prompt_builder import RepositoryReport, YesNoPartial


# Tests for RepositoryReport with default values.
def test_structure_defaults(default_report):
    """
    Tests that the report structure defaults are as expected.

    Args:
        default_report: The default report object to test.

    Returns:
        None
    """
    assert default_report.structure.compliance == "Unknown"
    assert default_report.structure.missing_files == []
    assert default_report.structure.organization == "Unknown"


def test_readme_defaults(default_report):
    """
    Asserts default values for readme attributes.

    Args:
        default_report: The report object to test.

    Returns:
        None

    """
    assert default_report.readme.readme_quality == "Unknown"
    assert default_report.readme.project_description == YesNoPartial.UNKNOWN
    assert default_report.readme.installation == YesNoPartial.UNKNOWN
    assert default_report.readme.usage_examples == YesNoPartial.UNKNOWN
    assert default_report.readme.contribution_guidelines == YesNoPartial.UNKNOWN
    assert default_report.readme.license_specified == YesNoPartial.UNKNOWN
    assert default_report.readme.badges_present == YesNoPartial.UNKNOWN


def test_documentation_defaults(default_report):
    """
    Tests that documentation defaults are set correctly.

    Args:
        default_report: The report object to test.

    Returns:
        None

    """
    assert default_report.documentation.tests_present == YesNoPartial.UNKNOWN
    assert default_report.documentation.docs_quality == "Unknown"
    assert default_report.documentation.outdated_content is False


def test_assessment_defaults(default_report):
    """
    Asserts default values for assessment attributes.

    Args:
        default_report: The report object to test.

    Returns:
        None
        This method asserts that the `key_shortcomings` attribute of the
        assessment within the provided report is equal to ["There are no critical issues"]
        and that the `recommendations` attribute is equal to ["No recommendations"].
    """
    assert default_report.assessment.key_shortcomings == [
        "There are no critical issues"
    ]
    assert default_report.assessment.recommendations == ["No recommendations"]


# Tests for RepositoryReport with custom-defined values.
def test_structure_custom(custom_report):
    """
    Asserts the structure attributes of a custom report.

    Args:
        custom_report: The custom report object to test.

    Returns:
        None
    """
    assert custom_report.structure.compliance == "Good"
    assert custom_report.structure.missing_files == ["setup.py"]
    assert custom_report.structure.organization == "Well structured"


def test_readme_custom(custom_report):
    """
    Asserts the quality and description of a README file.

    Args:
        custom_report: A custom report object containing readme information.

    Returns:
        None
        Performs assertions to validate the readme's quality is "Good"
        and project description is marked as YesNoPartial.YES.
    """
    assert custom_report.readme.readme_quality == "Good"
    assert custom_report.readme.project_description == YesNoPartial.YES


def test_documentation_custom(custom_report):
    """
    Checks custom report documentation attributes.

    Args:
        custom_report: The custom report object to validate.

    Returns:
        None
        Asserts that the documentation tests are present, quality is high, and content is outdated.
    """
    assert custom_report.documentation.tests_present == YesNoPartial.YES
    assert custom_report.documentation.docs_quality == "High"
    assert custom_report.documentation.outdated_content is True


def test_assessment_custom(custom_report):
    """
    Tests the custom assessment report.
    """
    assert custom_report.assessment.key_shortcomings == ["No CI/CD"]
    assert custom_report.assessment.recommendations == ["Add GitHub Actions"]


def test_extra_fields_ignored():
    """
    Tests that extra fields passed to the RepositoryReport are ignored.

        This test creates a RepositoryReport instance with an unexpected field
        and asserts that the field is not present as an attribute of the report object.

        Returns:
            None
    """
    report = RepositoryReport(extra_field="This should be ignored")
    assert not hasattr(report, "extra_field")
