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

    # is there an existing pyparsing element that has all alphas separated by spaces?
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

    # Parse the actual rule in the future:
    #   If a rule string is B34/S34:
    #     B34 means a cell is born if it has 3 or 4 neighbors.
    #     S34 means a cell survives if it has 3 or 4 neighbors.
    # x = 3, y = 3, rule = B3/S23
    # x = 3, y = 3
    _RULE: pp.ParserElement = pp.ZeroOrMore(
        pp.Keyword("rule").suppress()
        + pp.Suppress("=")
        + pp.Word(pp.printables + " ")
        + pp.Suppress(pp.line_end)
    ).set_results_name("rule")

    # bob$2bo$3o!
    #
    # 24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
    # obo$10bo5bo7bo$11bo3bo$12b2o!
    _DATA_ROWS: pp.ParserElement = pp.OneOrMore(
        (
            pp.OneOrMore(pp.Optional(_INT_NUMBER) + _CELL_STATES)
            + (
                _INT_NUMBER + pp.Literal("$")
                | pp.Literal("$").suppress()
                | pp.Literal("!").suppress()
            )
        ).set_results_name("data_rows", True)
    )

    _PARSER: pp.ParserElement = (
        pp.ZeroOrMore(_METADATA_LINE) + _HEADER + _RULE + _DATA_ROWS
    )

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        self._filename: str = file
        self._file: TextIOWrapper
        self.metadata: list[list[int | bool]]
        self.cols: int
        self.rows: int
        self.rule: str
        self.cell_array: list[list[bool]]

    def cells(self) -> list[list[bool]]:
        """Return an array of cells loaded from the file."""
        return self.cell_array

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        results: pp.ParseResults = RunLengthEncoded._PARSER.parse_file(self._file)
        self.metadata = results.metadata.as_list()  # type:ignore
        self.cols = int(results.header[0][1])  # type:ignore
        self.rows = int(results.header[1][1])  # type:ignore
        if results.rule:  # type: ignore
            self.rule = results.rule[0]  # type: ignore

        # initialise a row/col array of False to take the cells
        self.cell_array = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        # create iterator in order to add types
        row_iter: enumerate[list[int | str]] = enumerate(
            results.data_rows  # type:ignore
        )
        # it is necessary to keep track of an empty row offset for data like "7$"
        empty_rows: int = 0
        # iterate over the rows of data, equivalent to rows of cells
        for row_index, data_row in row_iter:
            col_index: int = 0
            # create another iterator so we can add types
            data_iter: enumerate[int | str] = enumerate(data_row)  # type:ignore
            # iterate of the data elements - note not equivalent to cells yet
            for data_index, data in data_iter:
                # if we get an int then we replicate that number of cells
                if isinstance(data, int):
                    # detect empty rows
                    if data_row[data_index + 1] == "$":
                        # because we are currently processing one of the empty rows add -1
                        empty_rows += data - 1
                    else:
                        cell: bool = data_row[data_index + 1] == "o"
                        # set the number of cells to the value
                        for _ in range(data):
                            self.cell_array[row_index + empty_rows][col_index] = cell
                            col_index += 1
                    # skip the next data value as we just "used" it
                    next(data_iter, None)
                # otherwise transform the data value to a cell value and store it
                else:
                    self.cell_array[row_index + empty_rows][col_index] = data == "o"
                    col_index += 1

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
        # make a more human readable list of the cell values
        cells: str = "\n".join(
            [
                " ".join(["■" if cell else "." for cell in cell_row])
                for cell_row in self.cell_array
            ]
        )
        return (
            f"{self.metadata}\n"
            + f"cols: {self.cols}, rows: {self.rows}, "
            + f"rule: {self.rule if hasattr(self, 'rule') else 'none'}\n"
            + f"cell_array:\n{cells}"
        )
