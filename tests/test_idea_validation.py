import pytest
from idea_validation import IdeaSummary, ValidationStep, IdeaValidation, export_idea_validation

def test_export_idea_validation():
    idea_summary = IdeaSummary("Test Idea", "This is a test idea")
    validation_steps = [ValidationStep("Step 1", "Passed"), ValidationStep("Step 2", "Failed")]
    idea_validation = IdeaValidation(idea_summary, validation_steps, 80)
    pdf_content = export_idea_validation(idea_validation)
    assert b"Test Idea" in pdf_content
    assert b"Step 1" in pdf_content
    assert b"Step 2" in pdf_content
    assert b"80" in pdf_content

def test_export_idea_validation_empty_steps():
    idea_summary = IdeaSummary("Test Idea", "This is a test idea")
    idea_validation = IdeaValidation(idea_summary, [], 80)
    pdf_content = export_idea_validation(idea_validation)
    assert b"Test Idea" in pdf_content
    assert b"[]" in pdf_content
    assert b"80" in pdf_content

def test_export_idea_validation_invalid_health_score():
    idea_summary = IdeaSummary("Test Idea", "This is a test idea")
    validation_steps = [ValidationStep("Step 1", "Passed"), ValidationStep("Step 2", "Failed")]
    idea_validation = IdeaValidation(idea_summary, validation_steps, -1)
    with pytest.raises(ValueError):
        export_idea_validation(idea_validation)
