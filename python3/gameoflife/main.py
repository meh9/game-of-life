"""The main game control and run loop."""

from math import floor
from time import perf_counter_ns
from blessed import Terminal
from blessed.keyboard import Keystroke

from gameoflife import GameOfLife, GameOfLifeSortedDict  # GameOfLifeArrays


class MainGame:
    """Manage the game."""

    HEADER_ROWS: int = 2
    FOOTER_ROWS: int = 8

    def __init__(self) -> None:
        """Initialise the game."""
        self._run: bool = True  # keep looping as long as this is true
        self._automatic: bool = False  # loop automatically and continuously when true
        self._sleep_time: float = 0.25  # seconds to sleep between loops in automatic
        self._origin_row: int = 0  # top row of the game view of the universe
        self._origin_col: int = 0  # left most cell of the game view of the universe
        self._term_width: int = 0  # save term width/height to detect if it changes
        self._term_height: int = 0
        self._live_count: int = 0  # track live cells for printing
        self._header_location: int = 0  # track the header location for moving it
        self._header_direction_left: bool = False
        self._last_gen_time: int = 0  # track how long time progress() took for printing
        self._edit_mode = False  # are editing right now?
        self._gol: GameOfLife  # game board and rules
        self._last_edit_location: tuple[int, int]  # save where the cursor was last

    def main(self) -> None:
        """Run the main game loop."""
        term = Terminal()
        # if initialising an Array type, figure out how to initialise to exact term.width/height
        # self.gol = GameOfLifeArrays(30, 60)
        self._gol = GameOfLifeSortedDict()
        # adding a glider for now as an example - add more? less? none?
        MainGame.add_glider(self._gol)
        self._live_count = self._gol.count_live_cells()

        # centre the initial board
        # TODO: do a better job of putting the initial board in the centre
        # one way is actually to put the initial cells in the centre as opposed to the board
        # For now, place 0,0 of the game board in the centre of the view.

        # This defines the View of the board in the coordinates of the board.
        # Another way to think of it is the origin_row/col defines how far away in board coords
        # the top left corner of the View is from 0,0 of the board.
        self._origin_row = 0 - floor(
            (term.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS) / 2
        )
        # divide in half again because we only print every other col
        self._origin_col = 0 - floor(term.width / 2 / 2)

        # TODO: this is getting complicated and hard to manage, can we simplify it significantly?
        # run the game
        with term.fullscreen(), term.cbreak():  # , term.hidden_cursor():
            while self._run:  # pragma: no cover
                # check if we need to clear screen and refresh - will always happen first runthrough
                # TODO: register a handler to refresh the screen on resize
                if self._term_width != term.width or self._term_height != term.height:
                    self._term_width = term.width
                    self._term_height = term.height
                    # reset cursor and clear the screen
                    print(term.home + term.clear, end="")
                    # print out the minimal game UI
                    self.print_ui(term)
                    self._header_location = floor(term.width / 2)
                    self.print_ui_update(term, False)
                    # set last edit location to be centre of screen
                    self._last_edit_location = (
                        floor(term.height / 2) - 1 - MainGame.HEADER_ROWS,
                        floor(term.width / 2) - 1,
                    )

                # print the game cells, taking care not to print over the bottom text
                self.print_game(term)

                # handle any potential keystrokes
                if self._automatic:
                    # progress the game a generation
                    start: int = perf_counter_ns()
                    self._live_count = self._gol.progress()
                    self._last_gen_time = perf_counter_ns() - start
                    # update the UI to reflect any changes
                    self.print_ui_update(term, True)
                    self.process_keystroke(term, False)
                else:
                    # only progress the game if the user asked for it
                    if self.process_keystroke(term, True):
                        start = perf_counter_ns()
                        self._live_count = self._gol.progress()
                        self._last_gen_time = perf_counter_ns() - start
                        # update the UI to reflect any changes
                        self.print_ui_update(term, True)

    def process_keystroke(
        self, term: Terminal, block: bool
    ) -> bool:  # pragma: no cover
        """
        Wait for a keystroke (with optional timeout) and process it.

        Return if the game should be progressed a generation due to user input.
        """
        # either block waiting for a keystroke or wait for sleep_time seconds
        key: Keystroke = term.inkey() if block else term.inkey(timeout=self._sleep_time)

        # process any potential key
        if key.is_sequence:
            match key.code:
                case term.KEY_ESCAPE:
                    self._run = False
                case term.KEY_UP:
                    if self._edit_mode:
                        print(term.move_up(1), end="")
                    else:
                        self._origin_row -= 1
                case term.KEY_DOWN:
                    if self._edit_mode:
                        print(term.move_down(1), end="")
                    else:
                        self._origin_row += 1
                case term.KEY_LEFT:
                    if self._edit_mode:
                        print(term.move_left(2), end="")
                    else:
                        self._origin_col -= 1
                case term.KEY_RIGHT:
                    if self._edit_mode:
                        print(term.move_right(2), end="")
                    else:
                        self._origin_col += 1
                case _:
                    pass  # do nothing with unrecognised keys
        else:
            match key:
                case " ":
                    if self._edit_mode:
                        row, col = term.get_location()
                        cell_row: int = row - MainGame.HEADER_ROWS + self._origin_row
                        cell_col: int = floor(col / 2) + self._origin_col
                        cell_state: bool | None = self._gol.get_cell(cell_row, cell_col)
                        if cell_state is not None:
                            self._gol.set_cell(cell_row, cell_col, not cell_state)
                        self.print_game(term)
                    else:
                        # progress the game a generation
                        return True
                case "e":
                    if self._edit_mode:
                        self._edit_mode = False
                        # save where the last edit mode was so we can return there
                        self._last_edit_location = term.get_location()
                        print(term.move_xy(0, 0), end="")
                        self.print_ui(term)
                    else:
                        self._automatic = False
                        self._edit_mode = True
                        self.print_ui(term)
                        # return to last edit location
                        print(term.move_x(self._last_edit_location[1]), end="")
                        print(term.move_y(self._last_edit_location[0]), end="")
                case "a":
                    if not self._edit_mode:
                        self._automatic = not self._automatic
                case "q":
                    self._run = False
                case "+" | "=":  # also accept "=" so we don't have use shift all the time
                    if not self._edit_mode:
                        self._sleep_time = self._sleep_time / 2
                        self.print_ui_update(term, False)
                case "-":
                    if not self._edit_mode:
                        self._sleep_time = self._sleep_time * 2
                        self.print_ui_update(term, False)
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

    def print_ui_update(self, term: Terminal, progress: bool) -> None:
        """Update things in the UI that needs updating; game name location, stats, etc."""
        # calculate moving header sectiong
        name: str = " ■ Conways's Game of Life □ "
        line: str = " ========================== "
        # move the name and underline from side to side, manage switching directions
        # this is pretty complicated, would be nice to do something simpler!
        half_width: int = floor(len(name) / 2)
        if progress:
            if self._header_direction_left:
                self._header_location -= 1
                if self._header_location - half_width < 0:
                    self._header_direction_left = False
                    self._header_location += 2
            else:
                self._header_location += 1
                if self._header_location >= term.width - half_width:
                    self._header_direction_left = True
                    self._header_location -= 2

        with term.location(0, 0), term.hidden_cursor():
            # header section
            print(term.move_x(self._header_location - half_width) + term.bold(name))
            print(term.move_x(self._header_location - half_width) + term.bold(line))
            # don't forget to update MainGame.HEADER_ROWS if making changes here!!!

        with term.location(0, term.height - MainGame.FOOTER_ROWS), term.hidden_cursor():
            print(term.bold("Statistics/Info") + term.move_down)
            print("Generation:    " + str(self._gol.generation) + "     ")
            print("Live cells:    " + str(self._live_count) + "     ")
            # intentional space on the end of "seconds " below
            print("Frame delay:   " + str(self._sleep_time) + " seconds    ")
            print("Progress time: " + str(self._last_gen_time) + " ns    ", end="")
            # future stats, max total of FOOTER_ROWS-2 due to current formatting
            # print("")
            # print("", end="")

    def print_game(self, term: Terminal) -> None:
        """Print the actual game board with cells from the GameOfLife instance."""
        with term.location(0, MainGame.HEADER_ROWS), term.hidden_cursor():
            row_list: list[str] = []
            max_rows: int = term.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS
            # because we separate all cells by a space we can only do half the number of cols
            max_cols: int = floor(term.width / 2)
            for view_row in range(max_rows):
                for view_col in range(max_cols):
                    cell: bool | None = self._gol.get_cell(
                        self._origin_row + view_row, self._origin_col + view_col
                    )
                    if cell is None:
                        row_list.append(" ")
                    else:
                        row_list.append("■" if cell else ".")
                        # □ ■ ▫ ◉ ○ ◌ ◎ ● ◯ ☉ ☐ ☻ ◦
                print(" ".join(row_list))
                row_list = []

    def print_ui(self, term: Terminal) -> None:
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
            if self._edit_mode:
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

    @staticmethod
    def add_glider(gol: GameOfLife) -> None:
        """Add a simple glider."""
        gol.set_cell(0, 1, True)
        gol.set_cell(1, 2, True)
        gol.set_cell(2, 0, True)
        gol.set_cell(2, 1, True)
        gol.set_cell(2, 2, True)
