from idea_generator import IdeaGenerator, Idea
import pytest

def test_add_interest():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    assert generator.interests == ["AI"]

def test_add_skill():
    generator = IdeaGenerator()
    generator.add_skill("Python")
    assert generator.skills == ["Python"]

def test_generate_ideas():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    generator.add_skill("Python")
    generator.generate_ideas()
    assert len(generator.ideas) == 1
    assert generator.ideas[0].name == "AI Python Tool"

def test_filter_ideas():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    generator.add_skill("Python")
    generator.generate_ideas()
    ideas = generator.filter_ideas(4, 7)
    assert len(ideas) == 1
    assert ideas[0].name == "AI Python Tool"

def test_sort_ideas():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    generator.add_skill("Python")
    generator.generate_ideas()
    ideas = generator.filter_ideas(4, 7)
    sorted_ideas = generator.sort_ideas(ideas, "relevance")
    assert len(sorted_ideas) == 1
    assert sorted_ideas[0].name == "AI Python Tool"

def test_sort_ideas_invalid_sort_by():
    generator = IdeaGenerator()
    generator.add_interest("AI")
    generator.add_skill("Python")
    generator.generate_ideas()
    ideas = generator.filter_ideas(4, 7)
    with pytest.raises(ValueError):
        generator.sort_ideas(ideas, "invalid")

def test_main():
    # This test is just to ensure the main function runs without errors
    from idea_generator import main
    main()
