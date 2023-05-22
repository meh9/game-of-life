"""Simple Conway's Game of Life implementation."""

from math import floor
from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict
from blessed import Terminal
from blessed.keyboard import Keystroke


FOOTER_ROWS: int = 7


def main() -> None:
    """Run through a simple glider progression. TODO: update this."""
    gol: GameOfLife = GameOfLifeArrays(12, 15)
    add_glider(gol)

    run: bool = True  # keep looping as long as this is true
    automatic: bool = False  # loop automatically and continuously when true
    sleep_time: float = 0.5  # seconds to sleep between loops in automatic
    origin_row: int = 0  # top row of the game view of the universe
    origin_col: int = 0  # left most cell of the game view of the universe
    term_width: int = 0
    term_height: int = 0
    live_count: int = 0

    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        start_row: int = 0
        max_rows: int = 0
        while run:
            # check if we need to clear screen and refresh - will always happen first runthrough
            if term_width != term.width or term_height != term.height:
                term_width = term.width
                term_height = term.height
                # reset cursor and clear the screen
                print(term.home + term.clear, end="")
                # print out the minimal game UI
                start_row, max_rows = print_ui(term)
                print_stats(term, gol.generation, gol.count_live_cells(), sleep_time)

            # print the game cells, taking care not to print over the bottom text
            print_game(
                term, gol, start_row, max_rows, term.width, origin_row, origin_col
            )

            # handle any potential keystrokes
            key: Keystroke | None = None  # the None is probably a terrible idea...
            if automatic:
                # progress the game a generation
                live_count = gol.progress()
                key = term.inkey(timeout=sleep_time)
            else:
                key = term.inkey()
            if key.is_sequence:
                match key.code:
                    case term.KEY_ESCAPE:
                        run = False
                    case term.KEY_UP:
                        origin_row -= 1
                    case term.KEY_DOWN:
                        origin_row += 1
                    case term.KEY_LEFT:
                        origin_col -= 1
                    case term.KEY_RIGHT:
                        origin_col += 1
                    case _:
                        pass  # do nothing with unrecognised keys
            else:
                match key:
                    case " ":
                        # progress the game a generation
                        live_count = gol.progress()
                    case "a":
                        automatic = not automatic
                    case "q":
                        run = False
                    case "+" | "=":  # also accept "=" so we don't have use shift all the time
                        sleep_time = sleep_time / 2
                    case "-":
                        sleep_time = sleep_time * 2
                    case _:
                        pass  # do nothing with unrecognised keys
            print_stats(term, gol.generation, live_count, sleep_time)


def print_stats(
    term: Terminal, generation: int, live_cells: int, sleep_time: float
) -> None:
    """TODO: implement and document."""
    with term.location(0, term.height - FOOTER_ROWS):
        print(term.bold("Statistics") + term.move_down)
        print("Generation:   " + str(generation))
        print("Live cells:   " + str(live_cells))
        print("Frame delay:  " + str(sleep_time) + " seconds", end="")
        # future stats
        # print("")
        # print("", end="")


def print_game(
    term: Terminal,
    gol: GameOfLife,
    start_row: int,
    max_rows: int,
    max_cols: int,
    origin_row: int,
    origin_col: int,
) -> None:
    """TODO: implement and document."""
    with term.location(0, start_row):
        row_list: list[str] = []
        # because we separate all cells by a space we can only do half the number of cols
        max_cols = floor(max_cols / 2)
        for view_row in range(max_rows):
            for view_col in range(max_cols):
                cell: bool | None = gol.get_cell(
                    origin_row + view_row, origin_col + view_col
                )
                if cell is None:
                    # TODO: probably want to replace this with a space eventually?
                    row_list.append(".")
                else:
                    row_list.append("■" if cell else "□")
            print(" ".join(row_list))
            row_list = []


def print_ui(term: Terminal) -> tuple[int, int]:
    """TODO: implement and document."""
    with term.location(0, 0):
        # set this to the number of rows being printed in the header below
        header_row_count: int = 2
        print(term.center(term.bold("■ Conways's Game of Life □")))
        print(term.center(term.bold("==========================")))

        print(term.move_xy(0, term.height - (FOOTER_ROWS + 1)))
        print(term.center(term.bold("Controls                   ")))
        print("=" * term.width)
        print(term.center("Quit:            q or ESC  "))
        print(term.center("Step forward:    <spacebar>"))
        print(term.center("Autorun On/Off:  a         "))
        print(term.center("Speed up/down:   +/-       "))
        print(term.center("Move the view:   ⇦⇧⇩⇨      "), end="")

        # TODO: new game (popup modal? select variant), add/remove cells
        return 2, term.height - FOOTER_ROWS - header_row_count

    """
    gol: GameOfLife = GameOfLifeArrays(12, 15)
    add_glider(gol)
    print(gol)
    gol.progress()
    print(gol)
    for _ in range(10001):
        gol.progress()
    print(gol)
    print("done")

    gol = GameOfLifeSortedDict()
    add_glider(gol)
    print(gol)
    gol.progress()
    print(gol)
    for _ in range(10001):
        gol.progress()
    print(gol)
    for _ in range(5):
        sleep_time: float = 0.5
        print("sleeping " + str(sleep_time) + "...")
        sleep(sleep_time)
        gol.progress()
        print(gol)
    """


def add_glider(gol: GameOfLife) -> None:
    """Add a simple glider."""
    gol.set_cell(0, 1, True)
    gol.set_cell(1, 2, True)
    gol.set_cell(2, 0, True)
    gol.set_cell(2, 1, True)
    gol.set_cell(2, 2, True)


if __name__ == "__main__":
    main()
