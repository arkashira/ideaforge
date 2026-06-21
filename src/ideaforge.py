"""Core Ideation Engine.

Provides a deterministic generator of software‑tool ideas based on niche,
budget and technical constraints.
"""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass(order=True)
class Idea:
    """A single software‑tool idea."""

    profitability_score: float = field(init=False, compare=True)
    description: str = field(compare=False)
    persona: str = field(compare=False)
    demand_score: int = field(compare=False)

    def __post_init__(self) -> None:
        # profitability is derived after demand_score is known
        self.profitability_score = float(self.demand_score)


def _deterministic_seed(
    niche_keywords: List[str],
    budget_range: Tuple[int, int],
    constraints: List[str],
) -> int:
    """Create a deterministic integer seed from the input parameters."""
    raw = "|".join(sorted(niche_keywords)) + f"|{budget_range[0]}-{budget_range[1]}" + "|" + "|".join(
        sorted(constraints)
    )
    return int(hashlib.sha256(raw.encode("utf-8")).hexdigest(), 16)


def _compute_profitability(demand: int, budget_range: Tuple[int, int]) -> float:
    """Composite profitability score.

    Heuristic:
    * Base is the demand score (0‑100).
    * Add a small bonus proportional to the upper budget bound.
    """
    max_budget = budget_range[1]
    bonus = (max_budget // 10_000) * 0.5  # 0.5 points per $10k
    return demand + bonus


def generate_ideas(
    niche_keywords: List[str],
    budget_range: Tuple[int, int],
    constraints: List[str],
    num_ideas: int = 5,
) -> List[Idea]:
    """Generate a ranked list of software‑tool ideas.

    Args:
        niche_keywords: List of niche terms (must contain at least one).
        budget_range: Tuple (min_budget, max_budget) where min ≤ max and both ≥ 0.
        constraints: List of technical constraints (may be empty).
        num_ideas: Number of ideas to generate (default 5).

    Returns:
        List of `Idea` objects sorted by descending profitability.

    Raises:
        ValueError: If `niche_keywords` is empty or budget range is invalid.
    """
    if not niche_keywords:
        raise ValueError("At least one niche keyword must be provided.")
    min_budget, max_budget = budget_range
    if min_budget < 0 or max_budget < 0 or min_budget > max_budget:
        raise ValueError("Invalid budget range.")

    seed = _deterministic_seed(niche_keywords, budget_range, constraints)
    rng = random.Random(seed)

    personas = ["Freelancers", "SMBs", "Enterprises", "Students", "Developers"]
    ideas: List[Idea] = []

    for _ in range(num_ideas):
        keyword = rng.choice(niche_keywords).title()
        constraint = rng.choice(constraints) if constraints else "any"
        description = f"{keyword} tool for {constraint} users."
        persona = rng.choice(personas)
        demand = rng.randint(0, 100)
        profitability = _compute_profitability(demand, budget_range)

        idea = Idea(
            description=description,
            persona=persona,
            demand_score=demand,
        )
        idea.profitability_score = profitability
        ideas.append(idea)

    # Sort by profitability descending
    ideas.sort(reverse=True)
    return ideas
