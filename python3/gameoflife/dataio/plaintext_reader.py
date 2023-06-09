"""File Loader for Plain Text file types."""

from io import TextIOWrapper
from types import TracebackType
import pyparsing as pp
from .file_reader import FileReader, FileReaderContextManager


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


class PlainTextReader(FileReaderContextManager):
    """Implements loading Plain Text data from files."""

    # !Name: Glider
    # !Author: Richard K. Guy
    # !The smallest, most common, and first discovered spaceship.
    # !www.conwaylife.com/wiki/index.php?title=Glider
    _METADATA_LINE: pp.ParserElement = pp.ZeroOrMore(
        (
            pp.AtLineStart("!").suppress()
            + (pp.Optional(pp.Word(pp.printables + " ")) + pp.line_end.suppress())
            .set_whitespace_chars(" \t")
            .set_results_name("metadata", True)
        )
    )

    _CELL_STATES: pp.ParserElement = pp.one_of(". O").set_whitespace_chars(" \t")

    # .O
    # ..O
    # OOO
    _DATA_ROWS: pp.ParserElement = pp.OneOrMore(
        (pp.ZeroOrMore(_CELL_STATES) + pp.line_end.suppress()).set_results_name(
            "data_rows", True
        )
    )

    _PARSER: pp.ParserElement = _METADATA_LINE + _DATA_ROWS

    def __init__(self, file: str) -> None:
        """Initialise the reader."""
        super().__init__(file)
        self._file: TextIOWrapper

    def __enter__(self) -> FileReader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        results: pp.ParseResults = PlainTextReader._PARSER.parse_file(self._file)
        self.metadata = (
            results.metadata.as_list() if results.metadata else []  # type:ignore
        )
        for row_index, row in enumerate(results.data_rows.as_list()):  # type:ignore
            for col_index, cell in enumerate(row):  # type:ignore
                if cell == "O":
                    self.cells.append((row_index, col_index))
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()
