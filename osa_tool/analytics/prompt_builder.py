from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class YesNoPartial(str, Enum):
    """
    Represents a yes/no/partial answer with additional states for unknown.

     This class provides a way to represent answers that are not simply true or false,
     allowing for partial agreement, disagreement, or an unknown state.

    """

    YES = "Yes"
    NO = "No"
    PARTIAL = "Partial"
    UNKNOWN = "Unknown"


class RepositoryStructure(BaseModel):
    """
    Analyzes the structure of a code repository.

     This class provides methods to assess various aspects of a repository's
     organization, including file compliance with naming conventions and
     identification of missing files based on expected structures.

    """

    compliance: str = Field("Unknown", description="Compliance with standard structure")
    missing_files: List[str] = Field(
        default_factory=list,
        description="List of missing critical files that impact project usability and clarity",
    )
    organization: str = Field(
        "Unknown",
        description="Evaluation of the overall organization of directories and files for maintainability and clarity",
    )


class ReadmeEvaluation(BaseModel):
    """
    Evaluates the quality and completeness of a project's README file.

    This class provides functionality to assess various aspects of a README,
    such as the presence of key sections (description, installation, usage),
    license information, badges, and overall readability. It aims to help
    maintainers ensure their projects have well-documented READMEs that are
    welcoming to contributors and users.
    """

    readme_quality: str = Field(
        "Unknown", description="Assessment of the README quality with a brief comment"
    )
    project_description: YesNoPartial = YesNoPartial.UNKNOWN
    installation: YesNoPartial = YesNoPartial.UNKNOWN
    usage_examples: YesNoPartial = YesNoPartial.UNKNOWN
    contribution_guidelines: YesNoPartial = YesNoPartial.UNKNOWN
    license_specified: YesNoPartial = YesNoPartial.UNKNOWN
    badges_present: YesNoPartial = YesNoPartial.UNKNOWN


class CodeDocumentation(BaseModel):
    """
    Analyzes code repositories for documentation quality and test coverage.

     This class provides a way to assess the presence of tests, the quality of
     documentation, and whether the content is up-to-date within a given codebase.
     It does not have any methods or attributes currently.

    """

    tests_present: YesNoPartial = YesNoPartial.UNKNOWN
    docs_quality: str = Field(
        "Unknown",
        description="Evaluation of the quality of code documentation, including API references, inline comments, and guides",
    )
    outdated_content: bool = Field(
        False,
        description="Flags whether the documentation contains outdated or misleading information",
    )


class OverallAssessment(BaseModel):
    """
    Provides an overall assessment of a software project.

     This class encapsulates the key shortcomings and recommendations
     identified during a review process, offering a consolidated view
     of the project's strengths and areas for improvement.

    """

    key_shortcomings: List[str] = Field(
        default_factory=lambda: ["There are no critical issues"],
        description="List of the most significant and critical issues that need to be addressed",
    )
    recommendations: List[str] = Field(
        default_factory=lambda: ["No recommendations"],
        description="Specific improvements to address issues or optimize the process",
    )


class RepositoryReport(BaseModel):
    """
    Analyzes an open-source repository and generates a report.

    This class takes a repository path as input, analyzes its structure,
    README content, documentation presence, and provides a basic assessment
    of the repository's health and quality.
    """

    structure: RepositoryStructure = Field(default_factory=RepositoryStructure)
    readme: ReadmeEvaluation = Field(default_factory=ReadmeEvaluation)
    documentation: CodeDocumentation = Field(default_factory=CodeDocumentation)
    assessment: OverallAssessment = Field(default_factory=OverallAssessment)

    class Config:
        extra = "ignore"
