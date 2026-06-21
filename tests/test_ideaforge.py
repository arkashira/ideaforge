import time
import pytest

from ideaforge import generate_ideas, Idea


def test_generate_ideas_happy_path():
    niche = ["finance", "analytics"]
    budget = (15000, 60000)
    constraints = ["cloud", "open-source"]

    start = time.time()
    ideas = generate_ideas(niche, budget, constraints, num_ideas=5)
    elapsed = time.time() - start

    # Timing requirement (well under 5 seconds)
    assert elapsed < 5.0

    # Correct number of ideas
    assert len(ideas) == 5

    # All items are Idea instances
    assert all(isinstance(i, Idea) for i in ideas)

    # Sorted by profitability descending
    for i in range(len(ideas) - 1):
        assert ideas[i].profitability_score >= ideas[i + 1].profitability_score

    # Fields validation
    for i in ideas:
        assert isinstance(i.description, str) and i.description
        assert isinstance(i.persona, str) and i.persona
        assert 0 <= i.demand_score <= 100
        assert isinstance(i.profitability_score, float)


def test_generate_ideas_deterministic():
    niche = ["health"]
    budget = (20000, 40000)
    constraints = ["mobile"]

    first = generate_ideas(niche, budget, constraints, num_ideas=3)
    second = generate_ideas(niche, budget, constraints, num_ideas=3)

    # Deterministic output: both calls produce identical ideas
    assert first == second


def test_generate_ideas_no_constraints():
    niche = ["education"]
    budget = (5000, 20000)
    constraints = []

    ideas = generate_ideas(niche, budget, constraints, num_ideas=2)

    for i in ideas:
        assert "any" in i.description  # fallback word when constraints empty


def test_generate_ideas_invalid_niche():
    with pytest.raises(ValueError) as exc:
        generate_ideas([], (1000, 5000), ["docker"])
    assert "At least one niche keyword" in str(exc.value)


def test_generate_ideas_invalid_budget():
    with pytest.raises(ValueError) as exc:
        generate_ideas(["gaming"], (10000, 5000), [])
    assert "Invalid budget range" in str(exc.value)
