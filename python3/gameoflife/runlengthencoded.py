"""File Loader for Run Length Encoded file types."""

from io import TextIOWrapper
from types import TracebackType
from gameoflife import FileLoader, FLContextManager
import pyparsing as pp


# pylint: disable=pointless-string-statement
""" 
#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed c/4.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""


class RunLengthEncoded(FLContextManager):
    """Implements loading Run Length Encoded data from files."""

    METADATA_LINE: pp.ParserElement = (
        (
            pp.AtLineStart("#").suppress()
            + pp.one_of("C c N O P R r")
            + pp.Word(pp.printables + " ")
            + pp.Suppress(pp.line_end)
        )
        .set_results_name("metadata", True)
        .set_name("metadata")
    )

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        self._filename: str = file
        self._file: TextIOWrapper

    def cells(self) -> list[list[bool]]:
        """Return an array of cells lopaded from the file."""
        return [[False]]

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        # print(METADATA)
        # parser:
        # parsed_file = parser.parse_file(self._file)
        # print(parsed_file)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()
