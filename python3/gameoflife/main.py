"""The main game control and run loop."""

from math import floor
from time import perf_counter_ns
from blessed import Terminal
from blessed.keyboard import Keystroke

from gameoflife import GameOfLife, GameOfLifeArrays  # , GameOfLifeSortedDict


class MainGame:
    """Manage the game."""

    HEADER_ROWS: int = 2
    FOOTER_ROWS: int = 8

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
        self.header_location: int = 0
        self.header_direction_left: bool = False
        self.last_gen_time: int = 0
        self.edit_mode = False

    def main(self) -> None:
        """Run the main game loop."""
        term = Terminal()
        # TODO: if initialising an Array type, initialise to the exact term.width/height
        gol: GameOfLife = GameOfLifeArrays(15, 20)
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
        # divide in half again because we only print every other col
        self.origin_col = 0 - floor(term.width / 2 / 2)

        # run the game
        with term.fullscreen(), term.cbreak():  # , term.hidden_cursor():
            start_row: int = 0
            max_rows: int = 0
            while self.run:
                # check if we need to clear screen and refresh - will always happen first runthrough
                # TODO: register a handler to refresh the screen on resize
                if self.term_width != term.width or self.term_height != term.height:
                    self.term_width = term.width
                    self.term_height = term.height
                    # reset cursor and clear the screen
                    print(term.home + term.clear, end="")
                    # print out the minimal game UI
                    start_row, max_rows = self.print_ui(term)
                    self.header_location = floor(term.width / 2)
                    self.print_ui_update(term, gol, False)

                # print the game cells, taking care not to print over the bottom text
                self.print_game(term, gol, start_row, max_rows)

                # handle any potential keystrokes
                if self.automatic:
                    # progress the game a generation
                    start: int = perf_counter_ns()
                    self.live_count = gol.progress()
                    self.last_gen_time = perf_counter_ns() - start
                    # update the UI to reflect any changes
                    self.print_ui_update(term, gol, True)
                    self.process_keystroke(term, False)
                else:
                    # only progress the game if the user asked for it
                    if self.process_keystroke(term, True):
                        start = perf_counter_ns()
                        self.live_count = gol.progress()
                        self.last_gen_time = perf_counter_ns() - start
                        # update the UI to reflect any changes
                        self.print_ui_update(term, gol, True)

    def process_keystroke(self, term: Terminal, block: bool) -> bool:
        """
        Wait for a keystroke (with optional timeout) and process it.

        Return if the game should be progressed a generation due to user input.
        """
        # either block waiting for a keystroke or wait for sleep_time seconds
        key: Keystroke = term.inkey() if block else term.inkey(timeout=self.sleep_time)

        # process any potential key
        if key.is_sequence:
            match key.code:
                case term.KEY_ESCAPE:
                    self.run = False
                case term.KEY_UP:
                    if self.edit_mode:
                        print(term.move_up(1), end="")
                    else:
                        self.origin_row -= 1
                case term.KEY_DOWN:
                    if self.edit_mode:
                        print(term.move_down(1), end="")
                    else:
                        self.origin_row += 1
                case term.KEY_LEFT:
                    if self.edit_mode:
                        print(term.move_left(1), end="")
                    else:
                        self.origin_col -= 1
                case term.KEY_RIGHT:
                    if self.edit_mode:
                        print(term.move_right(1), end="")
                    else:
                        self.origin_col += 1
                case _:
                    pass  # do nothing with unrecognised keys
        else:
            match key:
                case " ":
                    if self.edit_mode:
                        # TODO: finish edit mode: add/remove cell
                        pass
                    else:
                        # progress the game a generation
                        return True
                case "e":
                    if self.edit_mode:
                        self.edit_mode = False
                        print(term.move_xy(0, 0), end="")
                        self.print_ui(term)
                    else:
                        self.automatic = False
                        self.edit_mode = True
                        self.print_ui(term)
                        print(term.move_x(floor(term.width / 2) - 1), end="")
                        move_y: int = floor(term.height / 2) - 1 - MainGame.HEADER_ROWS
                        print(term.move_y(move_y), end="")
                case "a":
                    if not self.edit_mode:
                        self.automatic = not self.automatic
                case "q":
                    self.run = False
                case "+" | "=":  # also accept "=" so we don't have use shift all the time
                    if not self.edit_mode:
                        self.sleep_time = self.sleep_time / 2
                case "-":
                    if not self.edit_mode:
                        self.sleep_time = self.sleep_time * 2
                case _:
                    pass  # do nothing with unrecognised keys
        return False

    # layout model for UI top header moving text
    # |---------------------------------|  term.width = 50
    #                  h                   initial header_location = term.width / 2 = 25
    #           |----name----|             len(name) = 8
    #           p......h......             print location = header_location - (len(name) / 2) = 21
    # p......h......                       print location = header_location - (len(name) / 2) = 0
    # p......h......                       header_location = 0 + (len(name) / 2) = 4
    #                      p......h......  print location = term.width - len(name) = 42
    #                      p......h......  print location = header_location - (len(name) / 2) = 42
    #                      p......h......  header_location = term.width - (len(name) / 2) = 46

    def print_ui_update(self, term: Terminal, gol: GameOfLife, progress: bool) -> None:
        """Update things in the UI that needs updating; game name location, stats, etc."""
        # calculate moving header sectiong
        name: str = " ■ Conways's Game of Life □ "
        line: str = " ========================== "
        # TODO: this is pretty complicated, would be nice to do something simpler!
        half_width: int = floor(len(name) / 2)
        if progress:
            if self.header_direction_left:
                self.header_location -= 1
                if self.header_location - half_width < 0:
                    self.header_direction_left = False
                    self.header_location += 2
            else:
                self.header_location += 1
                if self.header_location >= term.width - half_width:
                    self.header_direction_left = True
                    self.header_location -= 2

        with term.location(0, 0), term.hidden_cursor():
            # header section
            print(term.move_x(self.header_location - half_width) + term.bold(name))
            print(term.move_x(self.header_location - half_width) + term.bold(line))
            # don't forget to update MainGame.HEADER_ROWS if making changes here!!!

        with term.location(0, term.height - MainGame.FOOTER_ROWS), term.hidden_cursor():
            print(term.bold("Statistics/Info") + term.move_down)
            print("Generation:    " + str(gol.generation))
            print("Live cells:    " + str(self.live_count))
            # intentional space on the end of "seconds " below
            print("Frame delay:   " + str(self.sleep_time) + " seconds ")
            print("Progress time: " + str(self.last_gen_time) + " ns ", end="")
            # future stats, max total of 6
            # print("")
            # print("", end="")

    def print_game(
        self, term: Terminal, gol: GameOfLife, start_row: int, max_rows: int
    ) -> None:
        """Print the actual game board with cells from the GameOfLife instance."""
        with term.location(0, start_row), term.hidden_cursor():
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

    def print_ui(self, term: Terminal) -> tuple[int, int]:
        """
        Print the main game UI.

        Returns a tuple with the 1st value being the row index to start printing the game board on,
        and the 2nd value being the maximum number of rows that the game board can print.
        """
        with term.location(0, 0), term.hidden_cursor():
            # footer section
            print(term.move_xy(0, term.height - (MainGame.FOOTER_ROWS + 1)))
            print(term.center(term.bold("Controls                   ")))
            print("=" * term.width)
            print(term.center("(ノಠ益ಠ)ノ彡┻━┻  q or ESC  "))  # intentional misalignment
            if self.edit_mode:
                print(term.center("Exit edit mode:  e         "))
                print(term.center("Live/dead cell:  <spacebar>"))
                print(term.center("Move cursor:     ⇦⇧⇩⇨      "))
                print(term.center("                           "))
                print(term.center("                           "), end="")
            else:
                print(term.center("Edit cells:      e         "))
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
