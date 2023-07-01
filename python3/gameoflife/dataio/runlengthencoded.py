"""File Loader for Run Length Encoded file types."""

from io import TextIOWrapper
from types import TracebackType
import pyparsing as pp
from .fileloader import FileLoader, FLContextManager


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
    _CELL_STATES: pp.ParserElement = pp.one_of(" ".join(list(pp.alphas)))

    # # N Glider
    # # O Richard K. Guy
    # #C www.conwaylife.com/wiki/index.php?title=Glider
    # #
    _METADATA_LINE: pp.ParserElement = pp.ZeroOrMore(
        (
            pp.AtLineStart("#").suppress()
            + pp.Optional(
                pp.one_of(" ".join(list(pp.printables)))
            ).set_whitespace_chars(" \t")
            + pp.Optional(pp.Word(pp.printables + " ")).set_whitespace_chars(" \t")
        ).set_results_name("metadata", True)
    )

    # x = 3, y = 3, rule = B3/S23
    # x = 3, y = 3
    _HEADER: pp.ParserElement = (
        pp.one_of("x y") + pp.Suppress("=") + _INT_NUMBER + pp.Optional(",").suppress()
    ).set_results_name("header", True) * 2

    # Parse the actual rule in the future:
    #   If a rule string is B34/S34:
    #     B34 means a cell is born if it has 3 or 4 neighbors.
    #     S34 means a cell survives if it has 3 or 4 neighbors.
    # x = 3, y = 3, rule = B3/S23
    # x = 3, y = 3
    _RULE: pp.ParserElement = pp.Optional(
        pp.Keyword("rule").suppress()
        + pp.Suppress("=")
        + pp.Word(pp.printables + " ").set_whitespace_chars(" \t")
    ).set_results_name("rule")

    # bob$2bo$3o!
    #
    # 24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
    # obo$10bo5bo7bo$11bo3bo$12b2o!
    _DATA_ROWS: pp.ParserElement = pp.OneOrMore(
        (
            pp.ZeroOrMore(pp.Optional(_INT_NUMBER) + _CELL_STATES)
            + (
                _INT_NUMBER + pp.Literal("$")
                | pp.Literal("$").suppress()
                | pp.Literal("!").suppress()
            )
        ).set_results_name("data_rows", True)
    )

    _PARSER: pp.ParserElement = _METADATA_LINE + _HEADER + _RULE + _DATA_ROWS

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        super().__init__(file)
        self._file: TextIOWrapper
        self._cols: int
        self._rows: int
        self._rule: str

    def __enter__(self) -> FileLoader:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        # start: int = perf_counter_ns()
        results: pp.ParseResults = RunLengthEncoded._PARSER.parse_file(self._file)
        # last_gen_time: int = perf_counter_ns() - start
        # print(f"Parsing finished in {round(last_gen_time / 1000)} µs")
        self.metadata = (
            results.metadata.as_list() if results.metadata else []  # type:ignore
        )
        self._cols = int(results.header[0][1])  # type:ignore
        self._rows = int(results.header[1][1])  # type:ignore
        if results.rule:  # type: ignore
            self._rule = results.rule[0]  # type: ignore

        # print("Starting to process parsed data...")
        # start = perf_counter_ns()
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
                    # is it a number of empty rows
                    if data_row[data_index + 1] == "$":
                        # track the number of empty rows, subtract 1 to avoid double counting it
                        # because we are currently processing the first empty row
                        empty_rows += data - 1
                    # if it is not an empty row
                    else:
                        live: bool = data_row[data_index + 1] == "o"
                        # if we are adding live cells add their coords to the list of cells
                        if live:
                            for _ in range(data):
                                self.cells.append((row_index + empty_rows, col_index))
                                col_index += 1
                        # "skip" dead cells by adding them as an offset to the col index
                        else:
                            col_index += data
                    # skip the next data value as we just "used" it
                    next(data_iter, None)
                # otherwise transform the data value to a cell value and store it
                else:
                    live = data_row[data_index] == "o"
                    if live:
                        self.cells.append((row_index + empty_rows, col_index))
                    col_index += 1
        # last_gen_time = perf_counter_ns() - start
        # print(f"Processing parsed data finished in {round(last_gen_time / 1000)} µs")
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
            super().__str__()
            + f"\ncols: {self._cols}, rows: {self._rows}\n"
            + f"rule: {self._rule if hasattr(self, '_rule') else 'none'}"
        )
