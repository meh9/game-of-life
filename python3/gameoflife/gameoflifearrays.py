"""Game of Life array based implementation."""

from gameoflife import GameOfLife


class GameOfLifeArrays(GameOfLife):
    """Implements Game of Life using two fixed size arrays, with universe wrap around."""

    def __init__(self, rows: int, cols: int) -> None:
        """Initialise the two parallel arrays."""
        super().__init__()
        self._a_array: list[list[bool]] = [
            [False for _ in range(cols)] for _ in range(rows)
        ]

    def progress(self) -> int:
        """Progress the game another generation."""
        # initialise a new array next_gen[[]] to be all False
        next_gen: list[list[bool]] = [
            [False for _ in range(len(self._a_array[0]))]
            for _ in range(len(self._a_array))
        ]
        count: int = 0

        # loop through every cell on the board and update the _b array with the next gen.
        for row_index, row_list in enumerate(self._a_array):
            for col_index, live in enumerate(row_list):
                num_neighbours: int = self._count_neighbours(row_index, col_index)
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in next gen.
                if num_neighbours == 3:
                    next_gen[row_index][col_index] = True
                    count += 1
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                elif live is True and num_neighbours == 2:
                    next_gen[row_index][col_index] = True
                    count += 1
                # 3. All other cells are dead in the next generation.
                # do nothing

        # swap the arrays
        self._a_array = next_gen
        self.generation += 1
        return count

    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the array to the given live value."""
        self._a_array[row][col] = live

    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""
        count: int = 0
        for row in self._a_array:
            for live in row:
                if live:
                    count += 1
        return count

    def get_cell(self, row: int, col: int) -> bool | None:
        """Return the live status of the given cell."""
        if (
            row >= 0
            and row < len(self._a_array)
            and col >= 0
            and col < len(self._a_array[0])
        ):
            return self._a_array[row][col]
        else:
            return None

    def _count_neighbours(self, row: int, col: int) -> int:
        """Count how many of the 8 neighbours of this cell are alive."""
        count = 0

        # check if we need to wrap around
        # if y==0 we can't decrement further, so wrap around to other extreme of array
        top: int = len(self._a_array) - 1 if row == 0 else row - 1
        # if y==a.length-1 we can't increment, so wrap around to 0
        bottom: int = 0 if row == len(self._a_array) - 1 else row + 1

        # if x==0 then we can't decrement further, so wrap around to other extreme of array
        left: int = len(self._a_array[0]) - 1 if col == 0 else col - 1
        # if x==a[0].length-1 we can't increment, so wrap around to 0
        right: int = 0 if col == len(self._a_array[0]) - 1 else col + 1

        # check all the neighbours
        count += self._a_array[top][left]
        count += self._a_array[top][col]
        count += self._a_array[top][right]
        count += self._a_array[row][left]
        # we don't do a[y][x] because it's the cell we're testing
        count += self._a_array[row][right]
        count += self._a_array[bottom][left]
        count += self._a_array[bottom][col]
        count += self._a_array[bottom][right]
        return count

    def __str__(self) -> str:
        """Return the a array as a formatted string."""
        # concise but unreadable double map version
        # return "\n".join(list(map(lambda r: "".join(list(map(lambda c: "■ " if c else "□ ", r))),
        #   self.a)))
        # expanded double for loop version
        str_list: list[str] = ["Generation: " + str(self.generation)]
        for row in self._a_array:
            row_list: list[str] = []
            for cell in row:
                row_list.append("■ " if cell else "□ ")
            str_list.append("".join(row_list))
        return "\n".join(str_list)
