"""Simple Conway's Game of Life implementation."""

from time import sleep
from sortedcontainers import SortedDict  # type: ignore

Coordinate = tuple[int, int]


def main() -> None:
    """Run through a simple glider progression."""
    # TODO: set up pytest
    # gol = GameOfLifeArrays(12, 15)
    # gol.a_array[0][1] = True
    # gol.a_array[1][2] = True
    # gol.a_array[2][0] = True
    # gol.a_array[2][1] = True
    # gol.a_array[2][2] = True
    # print(gol)
    # gol.progress()
    # print(gol)
    # for _ in range(10001):
    #     gol.progress()
    # print(gol)
    # print("done")

    gol = GameOfLifeSortedDict()
    gol.set_cell(0, 1, True)
    gol.set_cell(1, 2, True)
    gol.set_cell(2, 0, True)
    gol.set_cell(2, 1, True)
    gol.set_cell(2, 2, True)
    print(gol)
    gol.progress()
    print(gol)
    for _ in range(10001):
        gol.progress()
    print(gol)
    for _ in range(5):
        gol.progress()
        print(gol)
        sleep(0.5)


# TODO: sort out inheritance?
# TODO: split into their own modules/source files?
class GameOfLifeSortedDict:
    """Implements Game of Life using SortedDict (Red/Black "treemap" implementation)."""

    def __init__(self) -> None:
        """Initialise the map."""
        self.a_map: dict[Coordinate, bool] = SortedDict()
        self.generation = 0
        self.min_row = 0
        self.max_row = 0
        self.min_col = 0
        self.max_col = 0

    def __str__(self) -> str:
        """Iterate over all the cells and return a human readable string."""
        str_list: list[str] = ["Generation: " + str(self.generation)]
        for row in range(self.min_row, self.max_row + 1):  # add 1 to include last
            row_list: list[str] = []
            for col in range(self.min_col, self.max_col + 1):  # add 1 to include last
                if (row, col) in self.a_map:
                    row_list.append("■ " if self.a_map.get((row, col)) else "□ ")
                else:
                    row_list.append("  ")
            str_list.append("".join(row_list))
        return "\n".join(str_list)

    def progress(self) -> None:
        """Progress another generation."""
        self.min_row = 0
        self.max_row = 0
        self.min_col = 0
        self.max_col = 0
        b_map: dict[Coordinate, bool] = self.a_map
        self.a_map = SortedDict()
        # loop over every tracked cell
        for item in b_map.items():
            coords: Coordinate = item[0]
            live: bool = item[1]
            match self.live_neighbours(b_map, coords):
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                case 2:
                    if live:
                        self.set_cell(coords[0], coords[1], live)
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the
                # next generation.
                case 3:
                    self.set_cell(coords[0], coords[1], True)
                # 3. All other cells are dead in the next generation.
                case _:
                    pass
        self.generation += 1

    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the map to the given live value."""
        # track the min/max of cols
        if len(self.a_map) == 0:  # just set them first time around
            self.min_row = row
            self.max_row = row
            self.min_col = col
            self.max_col = col
        else:
            self.min_row = row if row < self.min_row else self.min_row
            self.max_row = row if row > self.max_row else self.max_row
            self.min_col = col if col < self.min_col else self.min_col
            self.max_col = col if col > self.max_col else self.max_col
        # if we are adding a live cell, also add dead neighbours if they don't already exist
        if live:
            self.a_map[(row, col)] = live
            # add all the dead neighbours if there is not a cell in the map already
            for neighbour in self.compute_neighbours(row, col):
                if neighbour not in self.a_map:
                    # recurse to set min/max
                    self.set_cell(neighbour[0], neighbour[1], False)
        elif (row, col) not in self.a_map:
            self.a_map[(row, col)] = False

    @classmethod
    def live_neighbours(cls, b_map: dict[Coordinate, bool], coords: Coordinate) -> int:
        """
        Count the number of live neighbours the cell at the given coords has.

        As a shortcut will only return up to the number 4, as we don't need to know any more for
        Game of Life.
        """
        live: int = 0
        for cell_coord in cls.compute_neighbours(coords[0], coords[1]):
            value = b_map.get(cell_coord)
            if value is not None and value:
                live += 1
        return live

    @classmethod
    def compute_neighbours(cls, row: int, col: int) -> list[Coordinate]:
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


class GameOfLifeArrays:
    """Implements Game of Life using two fixed size arrays, with universe wrap around."""

    def __init__(self, rows: int, cols: int) -> None:
        """Initialise the two parallel arrays."""
        self.a_array: list[list[bool]] = [
            [False for _ in range(cols)] for _ in range(rows)
        ]
        self.generation = 0

    def progress(self) -> None:
        """Progress the game another generation."""
        # initialise a new array next_gen[[]] to be all False
        next_gen: list[list[bool]] = [
            [False for _ in range(len(self.a_array[0]))]
            for _ in range(len(self.a_array))
        ]

        # loop through every cell on the board and update the _b array with the next gen.
        for row_index, row_list in enumerate(self.a_array):
            for col_index, live in enumerate(row_list):
                num_neighbours: int = self.count_neighbours(row_index, col_index)
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in next gen.
                if num_neighbours == 3:
                    next_gen[row_index][col_index] = True
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                elif live is True and num_neighbours == 2:
                    next_gen[row_index][col_index] = True
                # 3. All other cells are dead in the next generation.
                # do nothing

        # swap the arrays
        self.a_array = next_gen
        self.generation += 1

    def count_neighbours(self, row: int, col: int) -> int:
        """Count how many of the 8 neighbours of this cell are alive."""
        count = 0

        # check if we need to wrap around
        # if y==0 we can't decrement further, so wrap around to other extreme of array
        top: int = len(self.a_array) - 1 if row == 0 else row - 1
        # if y==a.length-1 we can't increment, so wrap around to 0
        bottom: int = 0 if row == len(self.a_array) - 1 else row + 1

        # if x==0 then we can't decrement further, so wrap around to other extreme of array
        left: int = len(self.a_array[0]) - 1 if col == 0 else col - 1
        # if x==a[0].length-1 we can't increment, so wrap around to 0
        right: int = 0 if col == len(self.a_array[0]) - 1 else col + 1

        # check all the neighbours
        count += self.a_array[top][left]
        count += self.a_array[top][col]
        count += self.a_array[top][right]
        count += self.a_array[row][left]
        # we don't do a[y][x] because it's the cell we're testing
        count += self.a_array[row][right]
        count += self.a_array[bottom][left]
        count += self.a_array[bottom][col]
        count += self.a_array[bottom][right]
        return count

    def __str__(self) -> str:
        """Return the a array as a formatted string."""
        # concise but unreadable double map version
        # return "\n".join(list(map(lambda r: "".join(list(map(lambda c: "■ " if c else "□ ", r))),
        #   self.a)))
        # expanded double for loop version
        str_list: list[str] = ["Generation: " + str(self.generation)]
        for row in self.a_array:
            row_list: list[str] = []
            for cell in row:
                row_list.append("■ " if cell else "□ ")
            str_list.append("".join(row_list))
        return "\n".join(str_list)


if __name__ == "__main__":
    main()
