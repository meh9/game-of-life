"""Simple Conway's Game of Life implementation."""

# from time import sleep
from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict
from blessed import Terminal
from blessed.keyboard import Keystroke


def main() -> None:
    """Run through a simple glider progression."""
    gol: GameOfLife = GameOfLifeArrays(12, 15)
    add_glider(gol)

    run: bool = True
    automatic: bool = False
    sleep_time: float = 0.5

    term = Terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # TODO: get height/width so we can check in the run loop if they've changed
        while run:
            print(term.home + term.clear, end="")
            start_row, max_rows = print_ui(term)
            gol.progress()
            with term.location(0, start_row):
                print_game(gol, max_rows)
            key: Keystroke | None = None  # the None is probably a terrible idea...
            if automatic:
                key = term.inkey(timeout=sleep_time)
            else:
                key = term.inkey()
            match key:
                case "a":
                    automatic = not automatic
                case "q" | "Q":
                    run = False
                case _:
                    # TODO: don't do this forever
                    print("Key: " + key)


def print_game(gol: GameOfLife, max_rows: int) -> None:
    """TODO: implement and documen."""
    print(gol)


def print_ui(term: Terminal) -> tuple[int, int]:
    """TODO: implement and document."""
    return 5, term.height

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
