"""Game of Life set implementation."""

from gameoflife import GameOfLife
from gameoflife import Coordinate


class GameOfLifeSet(GameOfLife):
    """Implements Game of Life using a Python set implementation."""

    def __init__(self) -> None:
        """Initialise the map."""
        super().__init__()
        self._cells: set[Coordinate] = set()
        self._min_row: int = 0
        self._max_row: int = 0
        self._min_col: int = 0
        self._max_col: int = 0

    def __str__(self) -> str:
        """Iterate over all the cells and return a human readable string."""
        str_list: list[str] = ["Generation: " + str(self.generation)]
        for row in range(self._min_row, self._max_row + 1):  # add 1 to include last
            row_list: list[str] = []
            for col in range(self._min_col, self._max_col + 1):  # add 1 to include last
                if (row, col) in self._cells:
                    row_list.append("■ " if (row, col) in self._cells else "□ ")
                else:
                    row_list.append("  ")
            str_list.append("".join(row_list))
        return "\n".join(str_list)

    def progress(self) -> int:
        """Progress another generation."""
        self._min_row = 0
        self._max_row = 0
        self._min_col = 0
        self._max_col = 0
        old_gen: set[Coordinate] = self._cells
        self._cells = set()
        checked_dead_cells: set[Coordinate] = set()
        count: int = 0
        # loop over every live cell
        for coords in old_gen:
            # check how many live neighbours we have
            num_live_neighbours: int = 0
            dead_neighbour_coords: list[Coordinate] = []
            for cell_coord in GameOfLifeSet._compute_neighbours(coords[0], coords[1]):
                if cell_coord in old_gen:
                    num_live_neighbours += 1
                else:
                    dead_neighbour_coords.append(cell_coord)

            # check if the current cell being processed should live
            match num_live_neighbours:
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                case 2:
                    self._cells.add(coords)
                    count += 1
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the
                # next generation.
                case 3:
                    self._cells.add(coords)
                    count += 1
                # 3. All other cells are dead in the next generation.
                case _:
                    pass

            # check if any of the dead neighbours should come alive
            for coords in dead_neighbour_coords:
                if coords not in checked_dead_cells:
                    num_live_neighbours = 0
                    for cell_coord in GameOfLifeSet._compute_neighbours(
                        coords[0], coords[1]
                    ):
                        if cell_coord in old_gen:
                            num_live_neighbours += 1
                    if num_live_neighbours == 3:
                        self._cells.add(coords)
                        count += 1
                checked_dead_cells.add(coords)

        self.generation += 1
        return count

    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the map to the given live value."""
        # only add the cell to the map if it is live
        if live:
            self._cells.add((row, col))
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

    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""
        return len(self._cells)

    def get_cell(self, row: int, col: int) -> bool | None:
        """
        Return the live status of the given cell.

        This implementation never returns None since the universe is "infinite".
        """
        return (row, col) in self._cells

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
