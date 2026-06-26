import json
from dataclasses import dataclass
from typing import List

@dataclass
class Idea:
    name: str
    relevance: int
    profitability: int

class IdeaGenerator:
    def __init__(self):
        self.interests = []
        self.skills = []
        self.ideas = []

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_skill(self, skill):
        self.skills.append(skill)

    def generate_ideas(self):
        self.ideas = []
        for interest in self.interests:
            for skill in self.skills:
                idea = Idea(f"{interest} {skill} Tool", 5, 8)
                self.ideas.append(idea)

    def filter_ideas(self, relevance_threshold, profitability_threshold):
        return [idea for idea in self.ideas if idea.relevance >= relevance_threshold and idea.profitability >= profitability_threshold]

    def sort_ideas(self, ideas, sort_by):
        if sort_by == "relevance":
            return sorted(ideas, key=lambda x: x.relevance, reverse=True)
        elif sort_by == "profitability":
            return sorted(ideas, key=lambda x: x.profitability, reverse=True)
        else:
            raise ValueError("Invalid sort_by parameter")

def main():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    generator.add_interest("Web Development")
    generator.add_skill("Python")
    generator.add_skill("JavaScript")
    generator.generate_ideas()
    ideas = generator.filter_ideas(4, 7)
    sorted_ideas = generator.sort_ideas(ideas, "relevance")
    print(json.dumps([{"name": idea.name, "relevance": idea.relevance, "profitability": idea.profitability} for idea in sorted_ideas], indent=4))

if __name__ == "__main__":
    main()
