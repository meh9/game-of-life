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

    _INT_NUMBER: pp.ParserElement = pp.Word(pp.nums).set_parse_action(  # type:ignore
        lambda t: [int(t[0])]  # type:ignore
    )

    _CELL_STATES: pp.ParserElement = pp.one_of(" ".join(c for c in pp.alphas))

    # N Glider
    # O Richard K. Guy
    # C www.conwaylife.com/wiki/index.php?title=Glider
    _METADATA_LINE: pp.ParserElement = (
        pp.AtLineStart("#").suppress()
        + pp.one_of("C c N O P R r")
        + pp.Word(pp.printables + " ")
        + pp.Suppress(pp.line_end)
    ).set_results_name("metadata", True)

    # x = 3, y = 3, rule = B3/S23
    # x = 3, y = 3
    _HEADER: pp.ParserElement = pp.OneOrMore(
        (
            pp.one_of("x y")
            + pp.Suppress("=")
            + _INT_NUMBER
            + pp.Optional(",").suppress()
        ).set_results_name("header", True)
    )

    # x = 3, y = 3, rule = B3/S23
    # x = 3, y = 3
    _RULE: pp.ParserElement = pp.ZeroOrMore(
        pp.Keyword("rule")
        + pp.Suppress("=")
        + pp.Word(pp.printables + " ")
        + pp.Suppress(pp.line_end)
    ).set_results_name("rule")

    # bob$2bo$3o!
    #
    # 24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
    # obo$10bo5bo7bo$11bo3bo$12b2o!
    _CELL_ROWS: pp.ParserElement = (
        pp.OneOrMore(
            (
                pp.OneOrMore(pp.Optional(_INT_NUMBER) + _CELL_STATES)
                + pp.Optional(pp.Literal("$").suppress())
            ).set_results_name("cell_rows", True)
        )
        + pp.Literal("!").suppress()
    )

    _PARSER: pp.ParserElement = pp.ZeroOrMore(_METADATA_LINE) + _HEADER + _RULE

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
        results: pp.ParseResults = RunLengthEncoded._PARSER.parse_file(self._file)
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
