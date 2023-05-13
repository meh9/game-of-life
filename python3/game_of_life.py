"""Simple Conway's Game of Life implementation."""


def main() -> None:
    """Run through a simple glider progression."""
    gol = GameOfLifeArrays(12, 15)
    gol.a_array[0][1] = True
    gol.a_array[1][2] = True
    gol.a_array[2][0] = True
    gol.a_array[2][1] = True
    gol.a_array[2][2] = True
    print(gol)
    gol.progress()
    print(gol)
    for _ in range(10000):
        gol.progress()
    print(gol)
    print("done")


class GameOfLifeArrays:
    """Implements Game of Life using two arrays fixed size arrays, with universe wrap around."""

    def __init__(self, rows: int, cols: int) -> None:
        """Initialise the two parallel arrays."""
        self.a_array: list[list[bool]] = [
            [False for _ in range(cols)] for _ in range(rows)
        ]
        self.iteration = 0

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
                if num_neighbours is 3:
                    next_gen[row_index][col_index] = True
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                elif live is True and num_neighbours == 2:
                    next_gen[row_index][col_index] = True
                # 3. All other cells are dead in the next generation.
                # do nothing

        # swap the arrays
        self.a_array = next_gen
        self.iteration += 1

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
        col_list: list[str] = ["Iteration: " + str(self.iteration)]
        for row in self.a_array:
            row_list: list[str] = []
            for cell in row:
                row_list.append("■ " if cell else "□ ")
            col_list.append("".join(row_list))
        return "\n".join(col_list)


if __name__ == "__main__":
    main()
