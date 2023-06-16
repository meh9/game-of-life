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
        super().__init__(file)
        self._file: TextIOWrapper

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
