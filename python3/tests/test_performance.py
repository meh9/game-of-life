"""Performance tests for all the Conway's Game of Life implementations."""

# from gameoflife import GameOfLife, GameOfLifeDict
import pytest

pytestmark: pytest.MarkDecorator = pytest.mark.performance


def test_dict_progress() -> None:
    """Performance test goes here."""
