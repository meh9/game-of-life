"""Game of Life sorted dict implementation."""

from sortedcontainers import SortedDict  # type: ignore
from gameoflife import GameOfLife

Coordinate = tuple[int, int]


class GameOfLifeSortedDict(GameOfLife):
    """Implements Game of Life using SortedDict (Red/Black "treemap" implementation)."""

    def __init__(self) -> None:
        """Initialise the map."""
        self._a_map: dict[Coordinate, bool] = SortedDict()
        self._generation: int = 0
        self._min_row: int = 0
        self._max_row: int = 0
        self._min_col: int = 0
        self._max_col: int = 0

    def __str__(self) -> str:
        """Iterate over all the cells and return a human readable string."""
        str_list: list[str] = ["Generation: " + str(self._generation)]
        for row in range(self._min_row, self._max_row + 1):  # add 1 to include last
            row_list: list[str] = []
            for col in range(self._min_col, self._max_col + 1):  # add 1 to include last
                if (row, col) in self._a_map:
                    row_list.append("■ " if self._a_map.get((row, col)) else "□ ")
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
        b_map: dict[Coordinate, bool] = self._a_map
        self._a_map = SortedDict()
        count: int = 0
        # loop over every tracked cell
        for item in b_map.items():
            coords: Coordinate = item[0]
            live: bool = item[1]
            match GameOfLifeSortedDict._live_neighbours(b_map, coords):
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                case 2:
                    if live:
                        self.set_cell(coords[0], coords[1], live)
                        count += 1
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the
                # next generation.
                case 3:
                    self.set_cell(coords[0], coords[1], True)
                    count += 1
                # 3. All other cells are dead in the next generation.
                case _:
                    pass
        self._generation += 1
        return count

    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the map to the given live value."""
        # track the min/max of cols
        if len(self._a_map) == 0:  # just set them first time around
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
            self._a_map[(row, col)] = live
            # add all the dead neighbours if there is not a cell in the map already
            for neighbour in GameOfLifeSortedDict._compute_neighbours(row, col):
                if neighbour not in self._a_map:
                    # recurse to set min/max
                    self.set_cell(neighbour[0], neighbour[1], False)
        elif (row, col) not in self._a_map:
            self._a_map[(row, col)] = False

    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""
        count: int = 0
        for live in self._a_map.values():
            if live:
                count += 1
        return count

    def get_cell(self, row: int, col: int) -> bool | None:
        """
        Return the live status of the given cell.

        This implementation never returns None since the universe is "infinite".
        """
        live: bool | None = self._a_map.get((row, col))
        if live is None:
            return False
        return live

    @staticmethod
    def _live_neighbours(b_map: dict[Coordinate, bool], coords: Coordinate) -> int:
        """
        Count the number of live neighbours the cell at the given coords has.

        As a shortcut will only return up to the number 4, as we don't need to know any more for
        Game of Life.
        """
        live_count: int = 0
        for cell_coord in GameOfLifeSortedDict._compute_neighbours(
            coords[0], coords[1]
        ):
            live: bool | None = b_map.get(cell_coord)
            if live is not None and live:
                live_count += 1
            # if there's more than 3 we're done
            if live_count > 3:
                return live_count
        return live_count

    @staticmethod
    def _compute_neighbours(row: int, col: int) -> list[Coordinate]:
        """Compute the coordinates of all the neighbours of the given cell."""
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

    @property
    def generation(self) -> int:
        """Return the current generation of the game."""
        return self._generation