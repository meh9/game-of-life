"""Simple Conway's Game of Life implementation."""

from math import floor
from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict
from blessed import Terminal
from blessed.keyboard import Keystroke


def main() -> None:
    """Run through a simple glider progression. TODO: update this."""
    gol: GameOfLife = GameOfLifeArrays(12, 15)
    add_glider(gol)

    run: bool = True  # keep looping as long as this is true
    automatic: bool = False  # loop automatically and continuously when true
    sleep_time: float = 0.5  # seconds to sleep between loops in automatic
    origin_row: int = 0  # top row of the game view of the universe
    origin_col: int = 0  # left most cell of the game view of the universe

    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # TODO: get height/width so we can check in the run loop if they've changed
        while run:
            # reset cursor and clear the screen
            # TODO: maybe we shouldn't, and just repaint things that change?
            print(term.home + term.clear, end="")
            # print out the minimal game UI
            start_row, max_rows = print_ui(term)

            # set the cursor to the start of the game area
            with term.location(0, start_row):
                # then print the game cells, taking care not to print over the bottom text
                print_game(gol, max_rows, term.width, origin_row, origin_col)

            # handle any potential keystrokes
            key: Keystroke | None = None  # the None is probably a terrible idea...
            if automatic:
                # progress the game a generation
                gol.progress()
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
                        gol.progress()
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


def print_game(
    gol: GameOfLife, max_rows: int, max_cols: int, origin_row: int, origin_col: int
) -> None:
    """TODO: implement and document."""
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
        print(term.center(term.bold("■ Conways's Game of Life □")))
        print(term.center(term.bold("==========================")))
        # the number of lines to be printed below +1
        print(term.move_xy(0, term.height - (7 + 1)))
        print(term.bold("Controls:"))
        print("==========================")
        print("Quit:             q or ESC")
        print("Step forward:     <spacebar>")
        print("Autorun On/Off:   a")
        print("Speed up/down:    +/-")
        print("Move the view:    ⇦⇧⇩⇨", end="")
        # TODO: new game (popup modal? select variant), add/remove cells
        # TODO: calculate max_rows properly - should it just be the num lines we print above?
        return 2, term.height - 9

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
