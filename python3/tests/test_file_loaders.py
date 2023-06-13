"""Tests for all the FileLoader implementations."""

# from pytest import raises
from gameoflife import create_loader, FileLoader, RunLengthEncoded
import pyparsing as pp


GLIDER: str = """\
#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed c/4.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""

HEADER_RULE: str = "x = 4, y = 5, rule = B3/S23"
HEADER_NO_RULE: str = "x = 4, y = 5"

GLIDER_DATA: str = "bob$2bo$3o!"
GOSPER_DATA: str = """\
24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
obo$10bo5bo7bo$11bo3bo$12b2o!
"""


def test_create_loader() -> None:
    """Test the create_loader function."""
    loader: FileLoader = create_loader("")
    # the below will change if and when we support different loader types
    assert loader.__class__ is RunLengthEncoded
    # with raises(ValueError):
    #     create_loader("")


# pylint: disable=protected-access
# pyright: reportPrivateUsage=false
class TestRunLengthEncoded:
    """Tests specifically for the class RunLengthEncoded."""

    def test_run_length_encoded(self) -> None:
        """Test the RunLengthEncoded file type."""
        with create_loader("../data/glider.rle") as loader:
            assert loader.__class__ is RunLengthEncoded
            assert loader.metadata  # type: ignore
            assert loader.cols  # type: ignore
            assert loader.rows  # type: ignore
            assert loader.rule  # type: ignore
            # the below will change when we actually have data
            assert loader.cells()[0][0] is False
            print(loader)
            assert (
                str(loader)
                == """\
[['N', 'Glider'], ['O', 'Richard K. Guy'], ['C', \
'The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed \
c/4.'], ['C', 'www.conwaylife.com/wiki/index.php?title=Glider']]
cols: 3, rows: 3, rule: B3/S23"""
            )

    def test_metadata_parser(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = pp.ZeroOrMore(
            RunLengthEncoded._METADATA_LINE
        ).parse_string(GLIDER)
        assert len(results) == 8
        assert results[0] == "N"
        assert results[1] == "Glider"
        assert results[-1] == "www.conwaylife.com/wiki/index.php?title=Glider"
        assert len(results.metadata) == 4  # type:ignore
        assert results.metadata[1][1] == "Richard K. Guy"  # type:ignore

    def test_header_rule_parser(self) -> None:
        """Test the HEADER parser."""
        results: pp.ParseResults = (
            RunLengthEncoded._HEADER + RunLengthEncoded._RULE
        ).parse_string(HEADER_RULE)
        assert results.header[0][1] == 4  # type:ignore
        assert results.header[1][1] == 5  # type:ignore
        assert results.rule[1] == "B3/S23"  # type:ignore

        results = (RunLengthEncoded._HEADER + RunLengthEncoded._RULE).parse_string(
            HEADER_NO_RULE
        )
        assert results.header[0][1] == 4  # type:ignore
        assert results.header[1][1] == 5  # type:ignore
        assert len(results.rule) == 0  # type:ignore

    def test_cell_rows_parser(self) -> None:
        """Test the CELL_ROWS parser."""
        results: pp.ParseResults = RunLengthEncoded._CELL_ROWS.parse_string(GLIDER_DATA)
        assert len(results.cell_rows) == 3  # type:ignore
        assert results.cell_rows[0].as_list() == ["b", "o", "b"]  # type:ignore
        assert results.cell_rows[2].as_list() == [3, "o"]  # type:ignore

        results = RunLengthEncoded._CELL_ROWS.parse_string(GOSPER_DATA)
        assert len(results.cell_rows) == 9  # type:ignore
        assert results.cell_rows[0].as_list() == [24, "b", "o"]  # type:ignore
        assert results.cell_rows[6].as_list() == [  # type:ignore
            10,
            "b",
            "o",
            5,
            "b",
            "o",
            7,
            "b",
            "o",
        ]
        assert results.cell_rows[8].as_list() == [12, "b", 2, "o"]  # type:ignore
