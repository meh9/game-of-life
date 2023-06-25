"""Game of Life dict implementation."""

from gameoflife import GameOfLife
from gameoflife import Coordinate


class GameOfLifeDict(GameOfLife):
    """Implements Game of Life using a Python dict implementation."""

    def __init__(self) -> None:
        """Initialise the map."""
        super().__init__()
        self._cells: dict[Coordinate, bool] = {}
        self._min_row: int
        self._max_row: int
        self._min_col: int
        self._max_col: int

    def __str__(self) -> str:
        """Iterate over all the cells and return a human readable string."""
        str_list: list[str] = ["Generation: " + str(self.generation)]
        for row in range(self._min_row, self._max_row + 1):  # add 1 to include last
            row_list: list[str] = []
            for col in range(self._min_col, self._max_col + 1):  # add 1 to include last
                if (row, col) in self._cells:
                    row_list.append("■ " if self._cells.get((row, col)) else "□ ")
                else:
                    row_list.append("  ")
            str_list.append("".join(row_list))
        return "\n".join(str_list)

    def progress(self) -> int:
        """Progress another generation."""
        old_gen: dict[Coordinate, bool] = self._cells
        self._cells = {}
        count: int = 0
        # loop over every tracked cell
        for coords, live in old_gen.items():
            match GameOfLifeDict._live_neighbours(old_gen, coords):
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                case 2:
                    if live:
                        self.set_cell(coords[0], coords[1], live)
                        count += 1
                    else:
                        pass  # required for code coverage? :/
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the
                # next generation.
                case 3:
                    self.set_cell(coords[0], coords[1], True)
                    count += 1
                # 3. All other cells are dead in the next generation.
                case _:
                    pass
        self.generation += 1
        return count

    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the map to the given live value."""
        # track the min/max of cols
        if len(self._cells) == 0:  # just set them first time around
            self._min_row = row
            self._max_row = row
            self._min_col = col
            self._max_col = col
        else:
            self._min_row = row if row < self._min_row else self._min_row
            self._max_row = row if row > self._max_row else self._max_row
            self._min_col = col if col < self._min_col else self._min_col
            self._max_col = col if col > self._max_col else self._max_col
        # if we are adding a live cell, also add dead neighbours if they don't already exist
        if live:
            self._cells[(row, col)] = live
            # add all the dead neighbours if there is not a cell in the map already
            for neighbour in GameOfLifeDict._compute_neighbours(row, col):
                if neighbour not in self._cells:
                    # recurse to set min/max
                    self.set_cell(neighbour[0], neighbour[1], False)
        else:
            self._cells[(row, col)] = False

    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""
        count: int = 0
        for cell in self._cells.values():
            if cell:
                count += 1
        return count

    def get_cell(self, row: int, col: int) -> bool | None:
        """
        Return the live status of the given cell.

        This implementation never returns None since the universe is "infinite".
        """
        live: bool | None = self._cells.get((row, col))
        if live is None:
            return False
        return live

    @staticmethod
    def _live_neighbours(cell_map: dict[Coordinate, bool], coords: Coordinate) -> int:
        """Count the number of live neighbours the cell at the given coords has."""
        live_count: int = 0
        for cell_coord in GameOfLifeDict._compute_neighbours(coords[0], coords[1]):
            if cell_map.get(cell_coord):
                live_count += 1
            # the funny thing is that doing the below actually slows the progress() down by 2.5%...
            # if there's more than 3 we're done
            # if live_count > 3:
            #     return live_count
        return live_count

    @staticmethod
    def _compute_neighbours(row: int, col: int) -> list[Coordinate]:
        """Compute the coordinates of all the neighbours of the given cell."""
        # pre-allocating these like this is 5% faster
        top: int = row - 1
        bottom: int = row + 1
        left: int = col - 1
        right: int = col + 1
        return [
            (top, left),
            (top, col),
            (top, right),
            (row, right),
            (bottom, right),
            (bottom, col),
            (bottom, left),
            (row, left),
        ]
