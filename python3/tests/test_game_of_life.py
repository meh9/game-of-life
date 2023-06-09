"""Tests for all the Conway's Game of Life implementations."""

from pytest import CaptureFixture, raises
from gameoflife import (
    MainGame,
    GameOfLife,
    GameOfLifeArrays,
    GameOfLifeDict,
    GameOfLifeSet,
)
from gameoflife.dataio.create_io import create_reader


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

    gol = GameOfLifeDict()
    set_cell_and_assert(gol, True, 1)
    set_cell_and_assert(gol, False, 0)
    set_cell_and_assert(gol, True, 1)

    gol = GameOfLifeSet()
    set_cell_and_assert(gol, True, 1)
    set_cell_and_assert(gol, False, 0)
    set_cell_and_assert(gol, True, 1)


def set_cell_and_assert(gol: GameOfLife, live: bool, num_live: int) -> None:
    """Set a cell and assert it stuck."""
    gol.set_cell(50, 55, live)
    assert gol.get_cell(50, 55) is live
    assert gol.count_live_cells() == num_live


class TestGameOfLifeSet:
    """Tests specifically for the class GameOfLifeSet."""

    def test_get_live_cells(self) -> None:
        """Test the get_live_cells method."""
        gol: GameOfLife = GameOfLifeSet()
        MainGame.add_glider(gol)
        assert gol.count_live_cells() == 5
        assert gol.get_live_cells() == [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeSet()
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
        gol: GameOfLife = GameOfLifeSet()
        gol.set_cell(10, 10, True)
        assert gol.get_cell(2, 2) is False
        assert gol.get_cell(10, 10) is True

    def test_str(self) -> None:
        """Test the str generation."""
        gol: GameOfLife = GameOfLifeSet()
        MainGame.add_glider(gol)
        print(gol)
        for _ in range(100):
            gol.progress()
            assert gol.count_live_cells() == 5
        print(gol)
        assert str(gol) == "Generation: 100\n  ■   \n    ■ \n■ ■ ■ "

    def test_match_case2(self) -> None:
        """Test a live cell with exactly 2 neighbours."""
        gol: GameOfLife = GameOfLifeSet()
        gol.set_cell(0, 0, True)
        gol.set_cell(0, 1, True)
        gol.set_cell(0, 2, True)
        gol.progress()
        assert gol.get_cell(-1, 1) is True
        assert gol.get_cell(1, 1) is True
        assert gol.get_cell(0, 0) is False
        assert gol.get_cell(0, 2) is False


class TestGameOfLifeArrays:
    """Tests specifically for the class GameOfLifeArrays."""

    def test_get_live_cells(self) -> None:
        """Test the get_live_cells method."""
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        MainGame.add_glider(gol)
        assert gol.count_live_cells() == 5
        assert gol.get_live_cells() == [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    def test_modulo_wrap(self) -> None:
        """Test that a patter larger than the array is wrapped correctly."""
        gol: GameOfLife = GameOfLifeArrays(12, 10)
        with create_reader("../data/test_wrap.cells") as reader:
            gol.add_cells(reader)
        assert (
            str(gol)
            == "Generation: 0\n"
            + "□ □ ■ □ □ ■ □ ■ □ □ \n"
            + "□ □ ■ □ □ □ ■ □ ■ □ \n"
            + "□ □ ■ □ □ □ □ ■ □ □ \n"
            + "□ □ □ □ □ □ □ □ ■ □ \n"
            + "□ □ □ □ □ □ □ □ □ ■ \n"
            + "■ □ □ □ □ □ □ □ □ □ \n"
            + "□ ■ □ □ □ □ □ □ □ □ \n"
            + "□ □ ■ □ □ □ □ □ □ □ \n"
            + "□ □ □ ■ □ □ □ □ □ □ \n"
            + "□ □ □ □ ■ □ □ □ □ □ \n"
            + "□ □ ■ □ □ ■ □ □ □ □ \n"
            + "□ □ ■ □ □ □ ■ □ □ □ "
        )

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
        assert (
            str(gol)
            == "Generation: 100\n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ ■ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ ■ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ ■ ■ ■ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ \n"
            + "□ □ □ □ □ □ □ □ □ □ □ □ □ □ □ "
        )


class TestGameOfLifeDict:
    """Tests specifically for the class GameOfLifeSortedDict."""

    def test_get_live_cells(self) -> None:
        """Test the get_live_cells method."""
        gol: GameOfLife = GameOfLifeDict()
        MainGame.add_glider(gol)
        assert gol.count_live_cells() == 5
        with raises(NotImplementedError):
            gol.get_live_cells()

    def test_glider(self) -> None:
        """Test that a simple glider progresses as expected."""
        gol: GameOfLife = GameOfLifeDict()
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
        gol: GameOfLife = GameOfLifeDict()
        gol.set_cell(10, 10, True)
        assert gol.get_cell(2, 2) is False
        assert gol.get_cell(10, 10) is True

    def test_str(self) -> None:
        """Test the str generation."""
        gol: GameOfLife = GameOfLifeDict()
        MainGame.add_glider(gol)
        for _ in range(100):
            gol.progress()
            assert gol.count_live_cells() == 5
        assert (
            str(gol)
            == "Generation: 100\n"
            + "  □ □ □   \n"
            + "  □ ■ □ □ \n"
            + "□ □ □ ■ □ \n"
            + "□ ■ ■ ■ □ \n"
            + "□ □ □ □ □ "
        )

    def test_match_case2(self) -> None:
        """Test a live cell with exactly 2 neighbours."""
        gol: GameOfLife = GameOfLifeDict()
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
    PRINT_UI_OUTPUT: str = (
        "\n"
        + "                                                     Controls                   \n"
        + "================================================================================\n"
        + "                                                     (ノº益º)ノ彡┻━┻  q or ESC  \n"
        + "                                                     Edit cells:      e         \n"
        + "                                                     Step forward:    <spacebar>\n"
        + "                                                     Autorun on/off:  a         \n"
        + "                                                     Speed up/down:   +/-       \n"
        + "                                                     Move the view:   ⇦⇧⇩⇨      "
    )

    # use string concatenation to highlight necessary trailing spaces
    PRINT_UI_EDIT_MODE_OUTPUT: str = (
        "\n"
        + "                                                     Controls                   \n"
        + "================================================================================\n"
        + "                                                     (ノº益º)ノ彡┻━┻  q or ESC  \n"
        + "                                                     Exit edit mode:  e         \n"
        + "                                                     Live/dead cell:  <spacebar>\n"
        + "                                                     Move cursor:     ⇦⇧⇩⇨      \n"
        + "                                                                                \n"
        + "                                                                                "
    )

    # use string concatenation to highlight necessary trailing spaces
    PRINT_UI_UPDATE_OUTPUT: str = (
        " ■ Conways's Game of Life □ \n"
        + " ========================== \n"
        + "Info\n"
        + "Generation:    0\n"
        + "Live cells:    5   \n"
        + "Frame delay:   250 ms    \n"
        + "Progress time: 0 µs   \n"
        + "Coords:        row:0 col:0  "
    )

    PRINT_GAME_OUTPUT: str = (
        "  ■                                                                            \n"
        + "    ■                                                                          \n"
        + "■ ■ ■                                                                          \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
        + "                                                                               \n"
    )

    @staticmethod
    def create_main_game() -> MainGame:
        """Create a MainGame and a Terminal and return them."""
        main: MainGame = MainGame(False, "../data/glider.rle")
        main._run = False
        main.main()
        return main

    def test_change_speed(self, capfd: CaptureFixture[str]) -> None:
        """Test the keyboard input functions."""
        main: MainGame = TestMainGame.create_main_game()
        # increasing speed shorts circuits to 0
        for _ in range(7):
            main._increase_speed()
            capfd.readouterr()
        assert main._sleep_time == 0.001953125
        main._increase_speed()
        capfd.readouterr()
        assert main._sleep_time == 0

        # decreasing speed goes back to 250 ms
        for _ in range(8):
            main._decrease_speed()
            capfd.readouterr()
        assert main._sleep_time == 0.25

        # decreasing speed goes to 64
        for _ in range(8):
            main._decrease_speed()
            capfd.readouterr()
        assert main._sleep_time == 64

    def test_update_screen_size(self, capfd: CaptureFixture[str]) -> None:
        """Test the update_screen_size function."""
        main: MainGame = TestMainGame.create_main_game()
        main.update_screen_size()
        capfd.readouterr()
        assert main._term_width == 80
        assert main._term_height == 25
        assert main._header_loc == 40
        assert main._last_edit_location == (8, 38)

    def test_initialise(self) -> None:
        """Test that we can even run at all."""
        assert MainGame(False)

    def test_initialise_wrap(self) -> None:
        """Test that we load different class when wrapping."""
        main: MainGame = MainGame(True)
        assert main
        assert main._gol.__class__.__name__ == GameOfLifeArrays(0, 0).__class__.__name__

    def test_load_rle_file(self, capfd: CaptureFixture[str]) -> None:
        """Test the loading of an RLE file."""
        main: MainGame = MainGame(False, "../data/glider.rle")
        main._run = False
        main.main()
        main.print_game()
        out: str = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_GAME_OUTPUT

    def test_load_plain_text_file(self, capfd: CaptureFixture[str]) -> None:
        """Test the loading of a Plain Text file."""
        main: MainGame = MainGame(True, "../data/glider.cells", 15, 4)
        main._run = False
        main.main()
        main._origin_col = -4
        main.print_game()
        out: str = capfd.readouterr()[0]
        assert (
            out
            == "        . ■ . .                                                                \n"
            + "        . . ■ .                                                                \n"
            + "        ■ ■ ■ .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
            + "        . . . .                                                                \n"
        )

    def test_print_ui(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui method."""
        main: MainGame = TestMainGame.create_main_game()
        main.print_ui()
        out: str = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_OUTPUT

    def test_print_ui_edit_mode(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui method when edit mode is on."""
        main: MainGame = TestMainGame.create_main_game()
        main._edit_mode = True
        main.print_ui()
        out: str = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_EDIT_MODE_OUTPUT

    def test_print_ui_update(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui_update method."""
        main: MainGame = TestMainGame.create_main_game()
        main.print_ui_update(False, main._gol.count_live_cells(), 0)
        out: str = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_UI_UPDATE_OUTPUT

    def test_print_ui_update_progress(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_ui_update method."""
        main: MainGame = TestMainGame.create_main_game()

        # test left edge turnaround
        main._header_loc = 15
        main._header_dir_left = True
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        capfd.readouterr()
        assert main._header_loc == 14
        assert main._header_dir_left is True
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        out: str = capfd.readouterr()[0]
        # the output is identical to the previos test_print_ui because term control characters
        # are not printed
        assert out == TestMainGame.PRINT_UI_UPDATE_OUTPUT
        assert main._header_loc == 15
        assert main._header_dir_left is False
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        assert main._header_loc == 16
        assert main._header_dir_left is False

        # test right edge turnaround
        main._header_loc = 66
        main.print_ui_update(True, main._gol.count_live_cells(), 0)
        assert main._header_loc == 65
        assert main._header_dir_left is True

    def test_print_game(self, capfd: CaptureFixture[str]) -> None:
        """Test the print_game method."""
        main: MainGame = TestMainGame.create_main_game()
        main.print_game()
        out: str = capfd.readouterr()[0]
        assert out == TestMainGame.PRINT_GAME_OUTPUT
