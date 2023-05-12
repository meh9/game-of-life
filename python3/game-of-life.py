def main() -> None:
    gol = GameOfLifeArrays(12, 15)
    gol._a[0][1] = True
    gol._a[1][2] = True
    gol._a[2][0] = True
    gol._a[2][1] = True
    gol._a[2][2] = True
    print(gol)
    gol.progress()
    print(gol)
    for _ in range(10000):
        gol.progress()
    print(gol)
    print("done")


class GameOfLifeArrays:
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialise the two parallel arrays.
        """
        self._a = [[False for _ in range(cols)] for _ in range(rows)]
        self._b = []
        self.iteration = 0

    def progress(self) -> None:
        """
        Progress the game another generation
        """
        # initialise the b array
        self._b = [[False for _ in range(len(self._a[0]))] for _ in range(len(self._a))]

        # loop through every cell on the board
        for row in range(len(self._a)):
            for col in range(len(self._a[row])):
                num_neighbours = self.count_neighbours(row, col)
                # 1. Any cell, dead or alive, with exactly 3 neighbours is alive in the next generation.
                if num_neighbours == 3:
                    self._b[row][col] = True
                # 2. A live cell with exactly 2 neighbours is alive in the next generation.
                elif self._a[row][col] == True and num_neighbours == 2:
                    self._b[row][col] = True
                # 3. All other cells are dead in the next generation.
                # do nothing

        # swap the arrays
        self._a = self._b
        self._b = None
        self.iteration += 1

    def count_neighbours(self, row: int, col: int) -> int:
        count = 0

        # check if we need to wrap around
        # if y==0 we can't decrement further, so wrap around to other extreme of array
        top = len(self._a) - 1 if row == 0 else row - 1
        # if y==a.length-1 we can't increment, so wrap around to 0
        bottom = 0 if row == len(self._a) - 1 else row + 1

        # if x==0 then we can't decrement further, so wrap around to other extreme of array
        left = len(self._a[0]) - 1 if col == 0 else col - 1
        # if x==a[0].length-1 we can't increment, so wrap around to 0
        right = 0 if col == len(self._a[0]) - 1 else col + 1

        # check all the neighbours
        count += self._a[top][left]
        count += self._a[top][col]
        count += self._a[top][right]
        count += self._a[row][left]
        # we don't do a[y][x] because it's the cell we're testing
        count += self._a[row][right]
        count += self._a[bottom][left]
        count += self._a[bottom][col]
        count += self._a[bottom][right]
        return count

    def __str__(self) -> str:
        """
        Returns the a array as a formatted string.
        """
        # concise double map version
        # return "\n".join(list(map(lambda r: "".join(list(map(lambda c: "■ " if c else "□ ", r))), self.a)))
        # expanded double for loop version
        l = ["Iteration: " + str(self.iteration)]
        for row in self._a:
            r = []
            for cell in row:
                r.append("■ " if cell else "□ ")
            l.append("".join(r))
        return "\n".join(l)


if __name__ == "__main__":
    main()
