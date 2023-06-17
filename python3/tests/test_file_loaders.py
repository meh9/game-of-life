"""Tests for all the FileLoader implementations."""

# from pytest import raises
from gameoflife import create_loader, FileLoader
from gameoflife.dataloaders import RunLengthEncoded, PlainText
import pyparsing as pp


GLIDER: str = """\
#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed c/4.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""

METADATA_NO_CONTENT: str = """\
#N next row has trailing space
#O 
#C
#
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
    loader: FileLoader = create_loader("file.rle")
    assert loader.__class__ is RunLengthEncoded
    loader = create_loader("file.cells")
    assert loader.__class__ is PlainText


# pylint: disable=protected-access
# pyright: reportPrivateUsage=false
class TestRunLengthEncoded:
    """Tests specifically for the class RunLengthEncoded."""

    def test_no_metadata(self) -> None:
        """Specific test for an RLE file with no metadata rows, and some other interesting things
        thrown in."""
        with create_loader("../data/no_metadata_test.rle") as loader:
            print(loader)
            assert loader.metadata == []

    def test_empty_row_data(self) -> None:
        """Specific test for testing data patterns like "7$" and "23$" which specifies a number of
        empty rows."""
        with create_loader("../data/t1point5infinitegrowth2.rle") as loader:
            # first two rows of data is (note "2$" at the end which skips a row of cells):
            #
            # 71b3o11b3o$70bo2bo10bo2bo$40b3o11b3o16bo4b3o6bo$40bo2bo10bo2bo15bo4bo
            # 2bo5bo$40bo6b3o4bo17bo4bo8bo$40bo5bo2bo4bo$41bo8bo4bo2$...
            # the skipped row is row index 7, so check it's all False
            assert loader.cells[7] == [False for _ in range(218)]
            # then check some random True
            assert loader.cells[6][40] is False
            assert loader.cells[6][41] is True
            assert loader.cells[6][42] is False
            assert loader.cells[8][71] is False
            assert loader.cells[8][72] is True
            assert loader.cells[8][73] is False

    def test_run_length_encoded(self) -> None:
        """Test the RunLengthEncoded file type."""
        # with create_loader("../data/Gosper_glider_gun.rle") as loader:
        with create_loader("../data/glider.rle") as loader:
            assert loader.__class__ is RunLengthEncoded
            assert loader.metadata  # type: ignore
            assert loader._cols  # type: ignore
            assert loader._rows  # type: ignore
            assert loader._rule  # type: ignore
            # the below will change when we actually have data
            assert loader.cells[0][0] is False
            assert loader.cells[0][1] is True
            assert (
                str(loader)
                == """\
RunLengthEncoded
file: ../data/glider.rle
metadata: [['N', 'Glider'], ['O', 'Richard K. Guy'], ['C', \
'The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed \
c/4.'], ['C', 'www.conwaylife.com/wiki/index.php?title=Glider']]
cells:
. ■ .
. . ■
■ ■ ■
cols: 3, rows: 3
rule: B3/S23"""
            )

    def test_metadata_no_content(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = RunLengthEncoded._METADATA_LINE.parse_string(
            METADATA_NO_CONTENT
        )
        assert results.metadata.as_list() == [  # type:ignore
            ["N", "next row has trailing space"],
            ["O"],
            ["C"],
            [],
            ["C", "www.conwaylife.com/wiki/index.php?title=Glider"],
        ]

    def test_metadata_parser(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = RunLengthEncoded._METADATA_LINE.parse_string(GLIDER)
        assert results.metadata.as_list() == [  # type:ignore
            ["N", "Glider"],
            ["O", "Richard K. Guy"],
            [
                "C",
                "The smallest, most common, and first discovered spaceship. Diagonal, has period "
                + "4 and speed c/4.",
            ],
            ["C", "www.conwaylife.com/wiki/index.php?title=Glider"],
        ]

    def test_header_rule_parser(self) -> None:
        """Test the HEADER parser."""
        results: pp.ParseResults = (
            RunLengthEncoded._HEADER + RunLengthEncoded._RULE
        ).parse_string(HEADER_RULE)
        assert results.header.as_list() == [["x", 4], ["y", 5]]  # type:ignore
        assert results.rule.as_list() == ["B3/S23"]  # type:ignore

        results = (RunLengthEncoded._HEADER + RunLengthEncoded._RULE).parse_string(
            HEADER_NO_RULE
        )
        assert results.header.as_list() == [["x", 4], ["y", 5]]  # type:ignore
        assert len(results.rule) == 0  # type:ignore

    def test_data_rows_parser(self) -> None:
        """Test the CELL_ROWS parser."""
        results: pp.ParseResults = RunLengthEncoded._DATA_ROWS.parse_string(GLIDER_DATA)
        assert results.data_rows.as_list() == [  # type:ignore
            ["b", "o", "b"],
            [2, "b", "o"],
            [3, "o"],
        ]

        results = RunLengthEncoded._DATA_ROWS.parse_string(GOSPER_DATA)
        assert len(results.data_rows) == 9  # type:ignore
        assert results.data_rows[0].as_list() == [24, "b", "o"]  # type:ignore
        assert results.data_rows[6].as_list() == [  # type:ignore
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
        assert results.data_rows[8].as_list() == [12, "b", 2, "o"]  # type:ignore
