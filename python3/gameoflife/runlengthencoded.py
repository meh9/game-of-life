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
        pp.AtLineStart("#").suppress()
        + pp.one_of("C c N O P R r")
        + pp.Word(pp.printables + " ")
        + pp.Suppress(pp.line_end)
    ).set_results_name("metadata", True)

    int_number: pp.ParserElement = pp.Word(pp.nums).set_parse_action(  # type:ignore
        lambda t: [int(t[0])]  # type:ignore
    )

    HEADER: pp.ParserElement = pp.OneOrMore(
        (
            pp.one_of("x y")
            + pp.Suppress("=")
            + int_number
            + pp.Optional(",").suppress()
        ).set_results_name("header", True)
    )

    RULE: pp.ParserElement = pp.ZeroOrMore(
        pp.Keyword("rule")
        + pp.Suppress("=")
        + pp.Word(pp.printables + " ")
        + pp.Suppress(pp.line_end)
    ).set_results_name("rule")

    PARSER: pp.ParserElement = pp.ZeroOrMore(METADATA_LINE) + HEADER + RULE

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        self._filename: str = file
        self._file: TextIOWrapper
        self.metadata: pp.ParseResults
        self.cols: int
        self.rows: int
        self.rule: str

    def cells(self) -> list[list[bool]]:
        """Return an array of cells lopaded from the file."""
        return [[False]]

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        results: pp.ParseResults = RunLengthEncoded.PARSER.parse_file(self._file)
        self.metadata = results.metadata  # type: ignore
        self.cols = results.header[0][1]  # type: ignore
        self.rows = results.header[1][1]  # type: ignore
        if results.rule:  # type: ignore
            self.rule = results.rule[1]  # type: ignore
        return self

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
        return (
            f"{self.metadata}\n"
            + f"cols: {self.cols}, rows: {self.rows}, "
            + f"rule: {self.rule if hasattr(self, 'rule') else 'none'}"
        )
