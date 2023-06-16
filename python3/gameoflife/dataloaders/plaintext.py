"""File Loader for Plain Text file types."""

from io import TextIOWrapper
from types import TracebackType
from gameoflife import FileLoader, FLContextManager
import pyparsing as pp


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


class PlainText(FLContextManager):
    """Implements loading Plain Text data from files."""

    # TODO: placeholder parser
    _PARSER: pp.ParserElement = pp.Literal(" ")

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        super().__init__()
        self._filename: str = file
        self._file: TextIOWrapper
        self.metadata: list[list[int | bool]]

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        results: pp.ParseResults = PlainText._PARSER.parse_file(self._file)
        self.metadata = results.metadata.as_list()  # type:ignore
        raise NotImplementedError()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()

    def __str__(self) -> str:
        """To string."""
        # make a more human readable list of the cell values
        cells_str: str = "\n".join(
            [
                " ".join(["■" if cell else "." for cell in cell_row])
                for cell_row in self.cells
            ]
        )
        return f"{self.metadata}\n" + f"cells:\n{cells_str}"
