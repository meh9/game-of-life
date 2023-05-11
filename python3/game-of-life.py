
def main() -> None:
    gol = GameOfLifeArrays(10, 10)
    gol.a[0][1] = True
    gol.a[1][2] = True
    gol.a[2][0] = True
    gol.a[2][1] = True
    gol.a[2][2] = True
    print (gol)
    print ("done")
    

class GameOfLifeArrays:
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialise the two parallel arrays.
        """
        self.a = [[False for _ in range(cols)] for _ in range(rows)]
        self.b = [[False for _ in range(cols)] for _ in range(rows)]

    def __str__(self) -> str:
        # concise double map version
        # return "\n".join(list(map(lambda r: "".join(list(map(lambda c: "■ " if c else "□ ", r))), self.a)))
        # expanded double for loop version
        l = []
        for row in self.a:
            r = []
            for cell in row:
                r.append("■ " if cell else "□ ")
            l.append("".join(r))
        return "\n".join(l)


if __name__ == "__main__":
    main()
