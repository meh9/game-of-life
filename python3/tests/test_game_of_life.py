"""Tests for all the Conway's Game of Life implementations."""

from pytest import CaptureFixture
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
        for _ in range(1000):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert gol.get_cell(0, 10) is True
        assert gol.get_cell(0, 11) is True
        assert gol.get_cell(0, 12) is True
        assert gol.get_cell(10, 11) is True
        assert gol.get_cell(11, 12) is True
        assert gol.generation == 1000

    def test_outofbounds(self) -> None:
        """Test that we get None when asking for a cell out of bounds."""
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        gol.set_cell(5, 6, True)
        assert gol.get_cell(5, 6) is True
        assert gol.get_cell(2, 2) is False
        assert gol.get_cell(20, 20) is None

    def test_str(self) -> None:
        """Test the str generation."""
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        MainGame.add_glider(gol)
        for _ in range(100):
            gol.progress()
            assert gol.count_live_cells() == 5
        print(gol)
        assert (
            str(gol)
            == """Generation: 100
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ ■ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ ■ □ □ 
□ □ □ □ □ □ □ □ □ □ ■ ■ ■ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ 
□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ """
        )


class TestGameOfLifeSortedDict:
    """Tests specifically for the class GameOfLifeSortedDict."""

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeSortedDict()
        MainGame.add_glider(gol)
        assert gol.count_live_cells() == 5
        for _ in range(1000):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert gol.get_cell(250, 251) is True
        assert gol.get_cell(251, 252) is True
        assert gol.get_cell(252, 250) is True
        assert gol.get_cell(252, 251) is True
        assert gol.get_cell(252, 252) is True
        assert gol.generation == 1000

    def test_outofbounds(self) -> None:
        """Test that we get False when asking for a cell out of bounds."""
        gol: GameOfLife = GameOfLifeSortedDict()
        gol.set_cell(10, 10, True)
        assert gol.get_cell(2, 2) is False
        assert gol.get_cell(10, 10) is True

    def test_str(self) -> None:
        """Test the str generation."""
        gol: GameOfLife = GameOfLifeSortedDict()
        MainGame.add_glider(gol)
        for _ in range(100):
            gol.progress()
            assert gol.count_live_cells() == 5
        print(gol)
        assert (
            str(gol)
            == """Generation: 100
  □ □ □   
  □ ■ □ □ 
□ □ □ ■ □ 
□ ■ ■ ■ □ 
□ □ □ □ □ """
        )

    def test_match_case2(self) -> None:
        """Test a live cell with exactly 2 neighbours."""
        gol: GameOfLife = GameOfLifeSortedDict()
        gol.set_cell(0, 0, True)
        gol.set_cell(0, 1, True)
        gol.set_cell(0, 2, True)
        gol.progress()
        assert gol.get_cell(-1, 1) is True
        assert gol.get_cell(1, 1) is True
        assert gol.get_cell(0, 0) is False
        assert gol.get_cell(0, 2) is False


# pylint: disable=protected-access
# pyright: reportPrivateUsage=false
class TestMainGame:
    """
    Tests specifically for MainGame.

    Testing this is really awful and will mean changing long strings of text all the time.
    Is there a better way to do this?
    """

    # use string concatenation to highlight necessary trailing spaces
    PRINT_UI_OUTPUT = (
        "\n"
        + "                          Controls                                              \n"
        + "================================================================================\n"
        + "                          (ノಠ益ಠ)ノ彡┻━┻  q or ESC                             \n"
        + "                          Edit cells:      e                                    \n"
        + "                          Step forward:    <spacebar>                           \n"
        + "                          Autorun On/Off:  a                                    \n"
        + "                          Speed up/down:   +/-                                  \n"
        + "                          Move the view:   ⇦⇧⇩⇨                                 "
    )

    PRINT_UI_EDIT_MODE_OUTPUT = (
        "\n                          Controls                                              \n"
        + "================================================================================\n"
        + "                          (ノಠ益ಠ)ノ彡┻━┻  q or ESC                             \n"
        + "                          Exit edit mode:  e                                    \n"
        + "                          Live/dead cell:  <spacebar>                           \n"
        + "                          Move cursor:     ⇦⇧⇩⇨                                 \n"
        + "                                                                                \n"
        + "                                                                                "
    )

    PRINT_UI_UPDATE_OUTPUT = (
        " ■ Conways's Game of Life □ \n"
        + " ========================== \n"
        + "Statistics/Info\n"
        + "Generation:    0\n"
        + "Live cells:    5   \n"
        + "Frame delay:   250 ms   \n"
        + "Progress time: 0 µs   "
    )

    PRINT_GAME_OUTPUT = (
        ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .\n"
        + """. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . ■ . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . ■ . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . ■ ■ ■ . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
"""
    )

    @staticmethod
    def create_main_game() -> MainGame:
        """Create a MainGame and a Terminal and return them."""
        main: MainGame = MainGame()
        main._run = False
        main.main()
        return main

    def test_load_rle_file(self, capfd: CaptureFixture[str]) -> None:
        """Test the loading of an RLE file."""
        main: MainGame = MainGame("../data/glider.rle")
        main._run = False
        main.main()
        main.print_game()
        out = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_GAME_OUTPUT

    def test_print_ui(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui method."""
        main = TestMainGame.create_main_game()
        main.print_ui()
        out = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_OUTPUT

    def test_print_ui_edit_mode(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui method when edit mode is on."""
        main = TestMainGame.create_main_game()
        main._edit_mode = True
        main.print_ui()
        out = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_EDIT_MODE_OUTPUT

    def test_print_ui_update(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui_update method."""
        main = TestMainGame.create_main_game()
        main.print_ui_update(False, main._gol.count_live_cells(), 0)
        out = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_UPDATE_OUTPUT

    def test_print_ui_update_progress(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui_update method."""
        main = TestMainGame.create_main_game()

        # test left edge turnaround
        main._header_loc = 13
        main._header_dir_left = True
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        out = capfd.readouterr()[0]
        # the output is identical to the previos test_print_ui because term control characters
        # are not printed
        assert out == TestMainGame.PRINT_UI_UPDATE_OUTPUT
        assert main._header_loc == 14
        assert main._header_dir_left is False
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        assert main._header_loc == 15
        assert main._header_dir_left is False

        # test right edge turnaround
        main._header_loc = 66
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        assert main._header_loc == 65
        assert main._header_dir_left is True

    def test_print_game(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_game method."""
        main = TestMainGame.create_main_game()
        main.print_game()
        out = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_GAME_OUTPUT