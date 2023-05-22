"""The main game control and run loop."""

from math import floor
from blessed import Terminal
from blessed.keyboard import Keystroke

from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict


class MainGame:
    """Manage the game."""

    HEADER_ROWS: int = 2
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

    def main(self) -> None:
        """Run the main game loop."""
        term = Terminal()
        # TODO: if initialising an Array type, initialise to the exact term.width/height
        gol: GameOfLife = GameOfLifeArrays(12, 15)
        # gol: GameOfLife = GameOfLifeSortedDict()
        MainGame.add_glider(gol)
        self.live_count = gol.count_live_cells()

        # centre the initial board
        # TODO: do a better job of putting the initial board in the centre
        # one way is actually to put the initial cells in the centre as opposed to the board
        # for now, place 0,0 of the game board in the centre of the view
        self.origin_row = 0 - floor(
            (term.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS) / 2
        )
        self.origin_col = 0 - floor(term.width / 2 / 2)

        # run the game
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
                    self.print_stats(term, gol)

                # print the game cells, taking care not to print over the bottom text
                self.print_game(term, gol, start_row, max_rows)

                # handle any potential keystrokes
                if self.automatic:
                    # progress the game a generation
                    self.live_count = gol.progress()
                    self.process_keystroke(term, False)
                else:
                    # only progress the game if the user asked for it
                    if self.process_keystroke(term, True):
                        self.live_count = gol.progress()

                # update the stats to reflect any changes
                self.print_stats(term, gol)

    def process_keystroke(self, term: Terminal, wait_for_key: bool) -> bool:
        """
        Wait for a keystroke (with optional timeout) and process it.

        Return if the game should be progressed a generation due to user input.
        """
        key: Keystroke = (
            term.inkey() if wait_for_key else term.inkey(timeout=self.sleep_time)
        )

        # process any potential key
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
                    return True
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
        return False

    def print_stats(self, term: Terminal, gol: GameOfLife) -> None:
        """Extract and print the statistics about the game from the game instance."""
        with term.location(0, term.height - MainGame.FOOTER_ROWS):
            print(term.bold("Statistics/Info") + term.move_down)
            print("Generation:   " + str(gol.generation))
            print("Live cells:   " + str(self.live_count))
            # intentional space on the end of "seconds " below
            print("Frame delay:  " + str(self.sleep_time) + " seconds ", end="")
            # future stats, max total of 5
            # print("")
            # print("", end="")

    def print_game(
        self, term: Terminal, gol: GameOfLife, start_row: int, max_rows: int
    ) -> None:
        """Print the actual game board with cells from the GameOfLife instance."""
        with term.location(0, start_row):
            row_list: list[str] = []
            # because we separate all cells by a space we can only do half the number of cols
            max_cols: int = floor(term.width / 2)
            for view_row in range(max_rows):
                for view_col in range(max_cols):
                    cell: bool | None = gol.get_cell(
                        self.origin_row + view_row, self.origin_col + view_col
                    )
                    if cell is None:
                        row_list.append(".")
                    else:
                        row_list.append("■" if cell else "□")
                print(" ".join(row_list))
                row_list = []

    @staticmethod
    def print_ui(term: Terminal) -> tuple[int, int]:
        """
        Print the main game UI.

        Returns a tuple with the 1st value being the row index to start printing the game board on,
        and the 2nd value being the maximum number of rows that the game board can print.
        """
        with term.location(0, 0):
            # header section
            # TODO: make the game name and ==== move when progressing the game
            # 1. could move both together side to side and then bounce and come back
            # 2. could move name one direction and ==== the other, then bounce and come back
            # 3. could
            print(term.center(term.bold("■ Conways's Game of Life □")))
            print(term.center(term.bold("==========================")))
            # don't forget to update MainGame.HEADER_ROWS if making changes here!!!

            # footer section
            print(term.move_xy(0, term.height - (MainGame.FOOTER_ROWS + 1)))
            print(term.center(term.bold("Controls                   ")))
            print("=" * term.width)
            print(term.center("(ノಠ益ಠ)ノ彡┻━┻  q or ESC  "))  # intentional misalignment
            print(term.center("Step forward:    <spacebar>"))
            print(term.center("Autorun On/Off:  a         "))
            print(term.center("Speed up/down:   +/-       "))
            print(term.center("Move the view:   ⇦⇧⇩⇨      "), end="")
            # don't forget to update MainGame.FOOTER_ROWS if making changes here!!!

            # TODO: new game (popup modal? select variant), add/remove cells
            return 2, term.height - MainGame.FOOTER_ROWS - MainGame.HEADER_ROWS

    @staticmethod
    def add_glider(gol: GameOfLife) -> None:
        """Add a simple glider."""
        gol.set_cell(0, 1, True)
        gol.set_cell(1, 2, True)
        gol.set_cell(2, 0, True)
        gol.set_cell(2, 1, True)
        gol.set_cell(2, 2, True)
