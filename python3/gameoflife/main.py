"""The main game control and run loop."""

from math import floor
from time import perf_counter_ns
from blessed import Terminal  # type:ignore
from blessed.keyboard import Keystroke  # type:ignore
from gameoflife import GameOfLife, GameOfLifeArrays, GameOfLifeSortedDict, create_loader


class MainGame:
    """Manage the game."""

    HEADER_ROWS: int = 2
    FOOTER_ROWS: int = 8

    def __init__(self, wrap: bool, file: str = "") -> None:
        """Initialise the game."""
        self._run: bool = True  # keep looping as long as this is true
        self._automatic: bool = False  # loop automatically and continuously when true
        self._sleep_time: float = 0.25  # seconds to sleep between loops in automatic
        self._origin_row: int = 0  # top row of the game view of the universe
        self._origin_col: int = 0  # left most cell of the game view of the universe
        self._term_width: int = 0  # save term width/height to detect if it changes
        self._term_height: int = 0
        self._header_loc: int = 0  # track the header location for moving it
        self._header_dir_left: bool = False
        self._edit_mode = False  # are editing right now?
        self._last_edit_location: tuple[int, int]  # save where the cursor was last
        self._t = Terminal()

        # infinite or wrapping universe
        if wrap:
            height: int = self._t.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS
            self._gol: GameOfLife = GameOfLifeArrays(height, floor(self._t.width / 2))
            print("wrap")
        else:
            self._gol = GameOfLifeSortedDict()
            print("infinite")

        if file:
            with create_loader(file) as loader:
                self._gol.add_cells(loader)
            # elif plain:
            #     pass

    def main(self) -> None:
        """Run the main game loop."""
        # centre the initial board
        # for now, disable this and just default to terminal 0,0 == game 0,0
        # TO DO: do a better job of putting the initial board in the centre
        # one way is actually to put the initial cells in the centre as opposed to the board
        # For now, place 0,0 of the game board in the centre of the view.
        # This defines the View of the board in the coordinates of the board.
        # Another way to think of it is the origin_row/col defines how far away in board coords
        # the top left corner of the View is from 0,0 of the board.
        # self._origin_row = 0 - floor(
        #     (self._t.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS) / 2
        # )
        # divide in half again because we only print every other col
        # self._origin_col = 0 - floor(self._t.width / 2 / 2)

        # TODO: this is getting complicated and hard to manage, can we simplify it significantly?
        # run the game
        with self._t.fullscreen(), self._t.cbreak():  # , term.hidden_cursor():
            while self._run:  # pragma: no cover
                # check if we need to clear screen and refresh - will always happen first runthrough
                # TODO: register a handler to refresh the screen on resize
                if (
                    self._term_width != self._t.width
                    or self._term_height != self._t.height
                ):
                    self._term_width = self._t.width
                    self._term_height = self._t.height
                    # reset cursor and clear the screen
                    print(self._t.home + self._t.clear, end="")
                    # print out the minimal game UI
                    self.print_ui()
                    self._header_loc = floor(self._t.width / 2)
                    self.print_ui_update(False, self._gol.count_live_cells(), None)
                    # init last edit location to be centre of view
                    row: int = (
                        floor(
                            # calculate the number of game rows in the view
                            (
                                self._t.height
                                - MainGame.HEADER_ROWS
                                - MainGame.FOOTER_ROWS
                            )
                            # find the centre of the game rows
                            / 2
                        )
                        # turn into 0-indexed terminal row
                        - 1
                        # offseet down by HEADER_ROWS
                        + MainGame.HEADER_ROWS
                    )
                    # find the centre of the terminal view, turn into 0-index terminal col
                    col: int = floor(self._t.width / 2) - 1
                    # column has to be even number as we only print cells in even columns
                    col = col if col % 2 == 0 else col - 1
                    self._last_edit_location = (row, col)

                # print the game cells, taking care not to print over the bottom text
                self.print_game()

                # handle any potential keystrokes
                if self._automatic:
                    # progress the game a generation
                    start: int = perf_counter_ns()
                    live_count: int = self._gol.progress()
                    last_gen_time: int = perf_counter_ns() - start
                    # update the UI to reflect any changes
                    self.print_ui_update(True, live_count, last_gen_time)
                    self.process_keystroke(False)
                else:
                    # only progress the game if the user asked for it
                    if self.process_keystroke(True):
                        start = perf_counter_ns()
                        live_count = self._gol.progress()
                        last_gen_time = perf_counter_ns() - start
                        # update the UI to reflect any changes
                        self.print_ui_update(True, live_count, last_gen_time)

    def process_keystroke(self, block: bool) -> bool:  # pragma: no cover
        """
        Wait for a keystroke (with optional timeout) and process it.

        Return if the game should be progressed a generation due to user input.
        """
        # either block waiting for a keystroke or wait for sleep_time seconds
        key: Keystroke = (
            self._t.inkey() if block else self._t.inkey(timeout=self._sleep_time)
        )

        # process any potential key
        if key.is_sequence:
            match key.code:
                case self._t.KEY_ESCAPE:
                    self._run = False
                case self._t.KEY_UP:
                    # TODO: moving to the edges of the view in edit mode does not move the view
                    if self._edit_mode:
                        print(self._t.move_up(1), end="")
                    else:
                        self._origin_row -= 1
                case self._t.KEY_DOWN:
                    if self._edit_mode:
                        print(self._t.move_down(1), end="")
                    else:
                        self._origin_row += 1
                case self._t.KEY_LEFT:
                    if self._edit_mode:
                        print(self._t.move_left(2), end="")
                    else:
                        self._origin_col -= 1
                case self._t.KEY_RIGHT:
                    if self._edit_mode:
                        print(self._t.move_right(2), end="")
                    else:
                        self._origin_col += 1
                case _:
                    pass  # do nothing with unrecognised keys
        else:
            match key:
                case " ":
                    if self._edit_mode:
                        row, col = self._t.get_location()
                        cell_row: int = row - MainGame.HEADER_ROWS + self._origin_row
                        cell_col: int = floor(col / 2) + self._origin_col
                        cell_state: bool | None = self._gol.get_cell(cell_row, cell_col)
                        if cell_state is not None:
                            self._gol.set_cell(cell_row, cell_col, not cell_state)
                        self.print_game()
                    else:
                        # progress the game a generation
                        return True
                case "e":
                    if self._edit_mode:
                        self._edit_mode = False
                        # save where the last edit mode was so we can return there
                        self._last_edit_location = self._t.get_location()
                        print(self._t.move_xy(0, 0), end="")
                        self.print_ui()
                    else:
                        self._automatic = False  # if we are running, stop
                        self._edit_mode = True
                        self.print_ui()
                        # return to last edit location
                        print(self._t.move_x(self._last_edit_location[1]), end="")
                        print(self._t.move_y(self._last_edit_location[0]), end="")
                case "a":
                    if not self._edit_mode:
                        self._automatic = not self._automatic
                case "q":
                    self._run = False
                case "+" | "=":  # also accept "=" so we don't have use shift all the time
                    if not self._edit_mode:
                        self._sleep_time = self._sleep_time / 2
                        self.print_ui_update(False, self._gol.count_live_cells(), None)
                case "-":
                    if not self._edit_mode:
                        self._sleep_time = self._sleep_time * 2
                        self.print_ui_update(False, self._gol.count_live_cells(), None)
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

    def print_ui_update(
        self, progress: bool, live_count: int, last_gen_time: int | None
    ) -> None:
        """Update things in the UI that needs updating; game name location, stats, etc."""
        # calculate moving header sectiong
        name: str = " ■ Conways's Game of Life □ "
        line: str = " ========================== "
        # move the name and underline from side to side, manage switching directions
        # this is pretty complicated, would be nice to do something simpler!
        half_width: int = floor(len(name) / 2)
        if progress:
            if self._header_dir_left:
                self._header_loc -= 1
                if self._header_loc - half_width < 0:
                    self._header_dir_left = False
                    self._header_loc += 2
            else:
                self._header_loc += 1
                if self._header_loc >= self._t.width - half_width:
                    self._header_dir_left = True
                    self._header_loc -= 2

        with self._t.location(0, 0), self._t.hidden_cursor():
            # header section
            print(self._t.move_x(self._header_loc - half_width) + self._t.bold(name))
            print(self._t.move_x(self._header_loc - half_width) + self._t.bold(line))
            # don't forget to update MainGame.HEADER_ROWS if making changes here!!!

        footer_start_row: int = self._t.height - MainGame.FOOTER_ROWS
        with self._t.location(0, footer_start_row), self._t.hidden_cursor():
            print(self._t.bold("Statistics/Info") + self._t.move_down)
            print(f"Generation:    {self._gol.generation}")
            print(f"Live cells:    {live_count}   ")
            # intentional space on the end of "seconds " below
            print(f"Frame delay:   {self._sleep_time*1000:.4g} ms   ")
            if last_gen_time is not None:
                print(f"Progress time: {round(last_gen_time / 1000)} µs   ", end="")
            # future stats, max total of FOOTER_ROWS-2 due to current formatting
            # print("")
            # print("", end="")

    def print_game(self) -> None:
        """Print the actual game board with cells from the GameOfLife instance."""
        with self._t.location(0, MainGame.HEADER_ROWS), self._t.hidden_cursor():
            row_list: list[str] = []
            max_rows: int = self._t.height - MainGame.HEADER_ROWS - MainGame.FOOTER_ROWS
            # because we separate all cells by a space we can only do half the number of cols
            max_cols: int = floor(self._t.width / 2)
            for view_row in range(max_rows):
                for view_col in range(max_cols):
                    cell: bool | None = self._gol.get_cell(
                        self._origin_row + view_row, self._origin_col + view_col
                    )
                    if cell is None:
                        # TODO: add test to exercise GameOfLifeArrays for this line if possible?
                        row_list.append(" ")
                    else:
                        row_list.append("■" if cell else ".")
                        # □ ■ ▫ ◉ ○ ◌ ◎ ● ◯ ☉ ☐ ☻ ◦
                print(" ".join(row_list))
                row_list = []

    def print_ui(self) -> None:
        """
        Print the main game UI.

        Returns a tuple with the 1st value being the row index to start printing the game board on,
        and the 2nd value being the maximum number of rows that the game board can print.
        """
        with self._t.location(0, 0), self._t.hidden_cursor():
            # footer section
            print(self._t.move_xy(0, self._t.height - (MainGame.FOOTER_ROWS + 1)))
            print(self._t.center(self._t.bold("Controls                   ")))
            print("=" * self._t.width)
            # TODO: table flip string is not fully compatible on e.g. latest Raspbian
            # intentional misalignment as some of these are wider on a terminal
            print(self._t.center("(ノಠ益ಠ)ノ彡┻━┻  q or ESC  "))
            if self._edit_mode:
                print(self._t.center("Exit edit mode:  e         "))
                print(self._t.center("Live/dead cell:  <spacebar>"))
                print(self._t.center("Move cursor:     ⇦⇧⇩⇨      "))
                print(self._t.center("                           "))
                print(self._t.center("                           "), end="")
            else:
                print(self._t.center("Edit cells:      e         "))
                print(self._t.center("Step forward:    <spacebar>"))
                print(self._t.center("Autorun On/Off:  a         "))
                print(self._t.center("Speed up/down:   +/-       "))
                print(self._t.center("Move the view:   ⇦⇧⇩⇨      "), end="")
            # don't forget to update MainGame.FOOTER_ROWS if making changes here!!!

    @staticmethod
    def add_glider(gol: GameOfLife) -> None:
        """Add a simple glider."""
        gol.set_cell(0, 1, True)
        gol.set_cell(1, 2, True)
        gol.set_cell(2, 0, True)
        gol.set_cell(2, 1, True)
        gol.set_cell(2, 2, True)
