"""The main game control and run loop."""

from math import floor
from blessed import Terminal
from blessed.keyboard import Keystroke

from gameoflife import GameOfLife, GameOfLifeArrays


class MainGame:
    """Manage the game."""

    FOOTER_ROWS: int = 7

    def __init__(self) -> None:
        """Initialise the game."""
        self.run: bool = True  # keep looping as long as this is true
        self.automatic: bool = False  # loop automatically and continuously when true
        self.sleep_time: float = 0.5  # seconds to sleep between loops in automatic
        self.origin_row: int = 0  # top row of the game view of the universe
        self.origin_col: int = 0  # left most cell of the game view of the universe
        self.term_width: int = 0
        self.term_height: int = 0
        self.live_count: int = 0

        self.gol: GameOfLife = GameOfLifeArrays(12, 15)
        MainGame.add_glider(self.gol)

    def main(self) -> None:
        """Run the main game loop."""
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            start_row: int = 0
            max_rows: int = 0
            while self.run:
                # check if we need to clear screen and refresh - will always happen first runthrough
                if self.term_width != term.width or self.term_height != term.height:
                    self.term_width = term.width
                    self.term_height = term.height
                    # reset cursor and clear the screen
                    print(term.home + term.clear, end="")
                    # print out the minimal game UI
                    start_row, max_rows = MainGame.print_ui(term)
                    MainGame.print_stats(
                        term,
                        self.gol.generation,
                        self.gol.count_live_cells(),
                        self.sleep_time,
                    )

                # print the game cells, taking care not to print over the bottom text
                MainGame.print_game(
                    term,
                    self.gol,
                    start_row,
                    max_rows,
                    term.width,
                    self.origin_row,
                    self.origin_col,
                )

                # handle any potential keystrokes
                key: Keystroke | None = None  # the None is probably a terrible idea...
                if self.automatic:
                    # progress the game a generation
                    self.live_count = self.gol.progress()
                    key = term.inkey(timeout=self.sleep_time)
                else:
                    key = term.inkey()
                if key.is_sequence:
                    match key.code:
                        case term.KEY_ESCAPE:
                            self.run = False
                        case term.KEY_UP:
                            self.origin_row -= 1
                        case term.KEY_DOWN:
                            self.origin_row += 1
                        case term.KEY_LEFT:
                            self.origin_col -= 1
                        case term.KEY_RIGHT:
                            self.origin_col += 1
                        case _:
                            pass  # do nothing with unrecognised keys
                else:
                    match key:
                        case " ":
                            # progress the game a generation
                            self.live_count = self.gol.progress()
                        case "a":
                            self.automatic = not self.automatic
                        case "q":
                            self.run = False
                        case "+" | "=":  # also accept "=" so we don't have use shift all the time
                            self.sleep_time = self.sleep_time / 2
                        case "-":
                            self.sleep_time = self.sleep_time * 2
                        case _:
                            pass  # do nothing with unrecognised keys
                MainGame.print_stats(
                    term, self.gol.generation, self.live_count, self.sleep_time
                )

    @staticmethod
    def print_stats(
        term: Terminal, generation: int, live_cells: int, sleep_time: float
    ) -> None:
        """TODO: implement and document."""
        with term.location(0, term.height - MainGame.FOOTER_ROWS):
            print(term.bold("Statistics") + term.move_down)
            print("Generation:   " + str(generation))
            print("Live cells:   " + str(live_cells))
            print("Frame delay:  " + str(sleep_time) + " seconds", end="")
            # future stats
            # print("")
            # print("", end="")

    @staticmethod
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

    @staticmethod
    def print_ui(term: Terminal) -> tuple[int, int]:
        """TODO: implement and document."""
        with term.location(0, 0):
            # set this to the number of rows being printed in the header below
            header_row_count: int = 2
            print(term.center(term.bold("■ Conways's Game of Life □")))
            print(term.center(term.bold("==========================")))

            print(term.move_xy(0, term.height - (MainGame.FOOTER_ROWS + 1)))
            print(term.center(term.bold("Controls                   ")))
            print("=" * term.width)
            print(term.center("Quit:            q or ESC  "))
            print(term.center("Step forward:    <spacebar>"))
            print(term.center("Autorun On/Off:  a         "))
            print(term.center("Speed up/down:   +/-       "))
            print(term.center("Move the view:   ⇦⇧⇩⇨      "), end="")

            # TODO: new game (popup modal? select variant), add/remove cells
            return 2, term.height - MainGame.FOOTER_ROWS - header_row_count

    @staticmethod
    def add_glider(gol: GameOfLife) -> None:
        """Add a simple glider."""
        gol.set_cell(0, 1, True)
        gol.set_cell(1, 2, True)
        gol.set_cell(2, 0, True)
        gol.set_cell(2, 1, True)
        gol.set_cell(2, 2, True)
