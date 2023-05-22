"""Simple Conway's Game of Life implementation."""

from gameoflife import MainGame


def main() -> None:
    """Run through a simple glider progression. TODO: update this."""
    game: MainGame = MainGame()
    game.main()

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


if __name__ == "__main__":
    main()
