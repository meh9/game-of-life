"""Tests for all the Conway's Game of Life implementations."""

from gameoflife import MainGame, GameOfLife, GameOfLifeArrays, GameOfLifeSortedDict


def test_set_unset_set() -> None:
    """
    Test that we can set, unset, then set a cell as live.

    GameOfLifeSortedDict had an issue where this wasn't working which was fixed in
    commit 47543a63a3364f1d00b802d74f8cc136aacc181a.
    """
    gol: GameOfLife = GameOfLifeArrays(100, 200)
    set_cell_and_assert(gol, True, 1)
    set_cell_and_assert(gol, False, 0)
    set_cell_and_assert(gol, True, 1)

    gol = GameOfLifeSortedDict()
    set_cell_and_assert(gol, True, 1)
    set_cell_and_assert(gol, False, 0)
    set_cell_and_assert(gol, True, 1)


def set_cell_and_assert(gol: GameOfLife, live: bool, num_live: int) -> None:
    """Set a cell and assert it stuck."""
    gol.set_cell(50, 55, live)
    assert gol.get_cell(50, 55) is live
    assert gol.count_live_cells() == num_live


class TestGameOfLifeArrays:
    """Tests specifically for the class GameOfLifeArrays."""

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        MainGame.add_glider(gol)
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
    """Tests specifically for the class GameOfLifeSortedDict."""

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeSortedDict()
        MainGame.add_glider(gol)
        assert gol.count_live_cells() == 5
        for _ in range(10000):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert gol.get_cell(2500, 2501) is True
        assert gol.get_cell(2501, 2502) is True
        assert gol.get_cell(2502, 2500) is True
        assert gol.get_cell(2502, 2501) is True
        assert gol.get_cell(2502, 2502) is True
