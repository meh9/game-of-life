"""Tests for all the Conway's Game of Life implementations."""

from game_of_life import add_glider, GameOfLife, GameOfLifeArrays, GameOfLifeSortedDict


class TestGameOfLifeArrays:
    """Tests for the GameOfLifeArrays class."""

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        add_glider(gol)
        assert gol.count_live_cells() == 5
        for _ in range(10000):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert gol.get_cell(4, 11) is True
        assert gol.get_cell(5, 12) is True
        assert gol.get_cell(6, 10) is True
        assert gol.get_cell(6, 11) is True
        assert gol.get_cell(6, 12) is True


class TestGameOfLifeSortedDict:
    """Tests for the class GameOfLifeSortedDict class."""

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeSortedDict()
        add_glider(gol)
        assert gol.count_live_cells() == 5
        for _ in range(10000):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert gol.get_cell(2500, 2501) is True
        assert gol.get_cell(2501, 2502) is True
        assert gol.get_cell(2502, 2500) is True
        assert gol.get_cell(2502, 2501) is True
        assert gol.get_cell(2502, 2502) is True
