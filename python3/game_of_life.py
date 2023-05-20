"""Simple Conway's Game of Life implementation."""

from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict
from blessed import Terminal
from blessed.keyboard import Keystroke


def main() -> None:
    """Run through a simple glider progression. TODO: update this."""
    gol: GameOfLife = GameOfLifeArrays(12, 15)
    add_glider(gol)

    run: bool = True
    automatic: bool = False
    sleep_time: float = 0.5

    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # TODO: get height/width so we can check in the run loop if they've changed
        while run:
            # reset cursor and clear the screen
            # TODO: maybe we shouldn't, and just repaint things that change?
            print(term.home + term.clear, end="")
            # print out the minimal game UI
            start_row, max_rows = print_ui(term)
            # progress the game a generation
            gol.progress()
            # set the cursor to the start of the game area
            with term.location(0, start_row):
                # then print the game cells, taking care not to print over the bottom text
                print_game(gol, max_rows)

            # handle any potential keystrokes
            key: Keystroke | None = None  # the None is probably a terrible idea...
            if automatic:
                key = term.inkey(timeout=sleep_time)
            else:
                key = term.inkey()
            if key.is_sequence:
                match key.code:
                    case term.KEY_ESCAPE:
                        run = False
                    case _:
                        pass  # do nothing with unrecognised keys
            else:
                match key:
                    case "a":
                        automatic = not automatic
                    case "q":
                        run = False
                    case "+" | "=":
                        sleep_time = sleep_time / 2
                    case "-":
                        sleep_time = sleep_time * 2
                    case _:
                        pass  # do nothing with unrecognised keys


def print_game(gol: GameOfLife, max_rows: int) -> None:
    """TODO: implement and document."""
    print(gol)


def print_ui(term: Terminal) -> tuple[int, int]:
    """TODO: implement and document."""
    with term.location(0, 0):
        print(term.center(term.bold("■ Conways's Game of Life □")), end="")
        print(term.center(term.bold("==========================")), end="")
        # the number of lines to be printed below +1
        print(term.move_xy(0, term.height - (5 + 1)))
        print(term.bold("Controls:"))
        print("==========================")
        print("Quit:             q or ESC")
        print("Autorun On/Off:   a")
        print("Speed up/down:    +/-", end="")
        # TODO: calculate max_rows properly - should it just be the num lines we print above?
        return 2, term.height - 8

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
