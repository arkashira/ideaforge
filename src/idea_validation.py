import json
from dataclasses import dataclass
from typing import List

@dataclass
class IdeaSummary:
    title: str
    description: str

@dataclass
class ValidationStep:
    step: str
    result: str

@dataclass
class IdeaValidation:
    idea_summary: IdeaSummary
    validation_steps: List[ValidationStep]
    health_score: int

    def to_dict(self):
        return {
            "idea_summary": {
                "title": self.idea_summary.title,
                "description": self.idea_summary.description
            },
            "validation_steps": [
                {"step": step.step, "result": step.result} for step in self.validation_steps
            ],
            "health_score": self.health_score
        }

    def generate_pdf(self) -> bytes:
        # Simulate PDF generation using a simple string representation
        pdf_content = json.dumps(self.to_dict(), indent=4).encode("utf-8")
        return pdf_content

def export_idea_validation(idea_validation: IdeaValidation) -> bytes:
    if idea_validation.health_score < 0 or idea_validation.health_score > 100:
        raise ValueError("Health score must be between 0 and 100")
    return idea_validation.generate_pdf()
