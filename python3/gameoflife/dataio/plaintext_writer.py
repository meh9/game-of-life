"""File Writer for Plain Text file types."""

from io import TextIOWrapper
from types import TracebackType
from gameoflife import Coordinate
from .file_writer import FileWriter, FileWriterContextManager


# pylint: disable=pointless-string-statement
""" 
!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO
"""


class PlainTextWriter(FileWriterContextManager):
    """Implements writing Plain Text data to files."""

    def __init__(self, file: str) -> None:
        """Initialise the reader."""
        super().__init__(file)
        self._file: TextIOWrapper

    def __enter__(self) -> FileWriter:
        """Enter context manager which causes the file to be parsed immediately."""
        # TODO: check if file exists?
        self._file = open(self._filename, "w", encoding="UTF-8")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()

    def write(self, metadata: list[str], cells: list[Coordinate]) -> None:
        """Write the Game of Life data to the file."""
        for data in metadata:
            self._file.write(f"!{data}\n")
        if cells:
            # find the min limits
            min_row: int = cells[0][0]
            min_col: int = cells[0][1]
            for row, col in cells:
                min_row = row if row < min_row else min_row
                min_col = col if col < min_col else min_col

            # keep track of where we wrote the last cell
            row_index: int = min_row
            col_index: int = min_col
            for row, col in cells:
                # get the difference in rows from the "last" cell to this one
                # this will be 0 when we're on the same row
                row_difference: int = row - row_index
                if row_difference > 0:
                    # write out the number of newlines required
                    self._file.write("\n" * row_difference)
                    # reset the col_index as we are on a new row
                    col_index = min_col
                # get the difference in cols from the "last" cell to this one
                col_difference: int = col - col_index
                # if there is a col difference then that is a dead cell gap
                if col_difference > 0:
                    self._file.write("." * col_difference)
                # finish by writing the live cell
                self._file.write("O")
                # update the index to point to the last cell +1 col of the cell we just wrote
                row_index = row
                col_index = col + 1
            self._file.write("\n")
