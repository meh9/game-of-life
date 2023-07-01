"""File loader abstract class specifying the interface for loading cells from a file."""

from abc import ABC, abstractmethod
from functools import reduce
from types import TracebackType
from gameoflife import Coordinate


class FileLoader(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    def __init__(self, file: str) -> None:
        """Initialise."""
        self._filename: str = file
        self.cells: list[Coordinate] = []
        self.metadata: list[list[int | bool]]

    @staticmethod
    def _coord_max(left: Coordinate, right: Coordinate) -> Coordinate:
        """Reduce function for getting the max bounds of cells."""
        left_row: int = left[0]
        left_col: int = left[1]
        right_row: int = right[0]
        right_col: int = right[1]
        return (
            left_row if left_row > right_row else right_row,
            left_col if left_col > right_col else right_col,
        )

    def __str__(self) -> str:
        """
        To str method default implementation.

        Sublasses might want to replace or augment this output.

        WARNING: for large patterns this will run out of memory as it tries to print a matrix.
        """
        # make a more human readable list of the cell values
        # first get the max row and col
        max_coords: Coordinate = reduce(FileLoader._coord_max, self.cells, (0, 0))
        # then initialise a 2d list of that size
        cell_matrix: list[list[bool]] = [
            [False for _ in range(max_coords[1] + 1)] for _ in range(max_coords[0] + 1)
        ]
        # then set all the live cells in that 2d list
        for row, col in self.cells:
            cell_matrix[row][col] = True
        # then turn that 2d list into a cell board string
        cells_str: str = "\n".join(
            [
                " ".join(["■" if cell else "." for cell in cell_row])
                for cell_row in cell_matrix
            ]
        )
        return (
            f"{type(self).__name__}\n"
            + f"file: {self._filename}\n"
            + f"metadata: {self.metadata}\n"
            + f"cells:\n{cells_str}"
        )

    # TO DO: add getting top-left coords, which will need new parsing too
    # Example: #R -22 -57
    # Gives the coordinates of the top-left corner of the pattern. RLE files produced by XLife
    # usually have this line, and the coordinates are usually negative, with the intention of
    # placing the centre of the pattern at the origin.


class FLContextManager(FileLoader):
    """ABC for adding context management to FileLoaders."""

    @abstractmethod
    def __enter__(self) -> FileLoader:
        """Enter context manager."""

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
