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

    # is there an existing pyparsing element that has all alphas separated by spaces?
    _CELL_STATES: pp.ParserElement = pp.one_of(". O").set_whitespace_chars(" \t")

    # bob$2bo$3o!
    #
    # 24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
    # obo$10bo5bo7bo$11bo3bo$12b2o!
    _DATA_ROWS: pp.ParserElement = pp.OneOrMore(
        (pp.OneOrMore(_CELL_STATES) + pp.line_end.suppress()).set_results_name(
            "data_rows", True
        )
    )

    _PARSER: pp.ParserElement = _METADATA_LINE + _DATA_ROWS

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        super().__init__(file)
        self._file: TextIOWrapper

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        results: pp.ParseResults = PlainText._PARSER.parse_file(self._file)
        self.metadata = results.metadata.as_list()  # type:ignore
        print(self.metadata)  # type:ignore
        print(results.data_rows.as_list())  # type:ignore
        self.cells = []
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()