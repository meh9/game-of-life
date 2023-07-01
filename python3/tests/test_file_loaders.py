"""Tests for all the FileLoader implementations."""

from pytest import raises
from gameoflife import create_loader, FileLoader
from gameoflife.dataio import RunLengthEncoded, PlainText
import pyparsing as pp


def test_create_loader() -> None:
    """Test the create_loader function."""
    loader: FileLoader = create_loader("file.rle")
    assert loader.__class__ is RunLengthEncoded
    loader = create_loader("file.cells")
    assert loader.__class__ is PlainText
    with raises(ValueError):
        create_loader("foo.bar")


# pylint: disable=protected-access
# pyright: reportPrivateUsage=false
class TestPlainText:
    """Tests specifically for the class PlainText."""

    def test_metadata_parser(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = PlainText._METADATA_LINE.parse_string(
            """\
!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO
"""
        )
        assert results.metadata.as_list() == [  # type:ignore
            ["Name: Glider"],
            ["Author: Richard K. Guy"],
            ["The smallest, most common, and first discovered spaceship."],
            ["www.conwaylife.com/wiki/index.php?title=Glider"],
        ]

    def test_data_rows_parser(self) -> None:
        """Test the CELL_ROWS parser."""
        results: pp.ParseResults = PlainText._DATA_ROWS.parse_string(
            """\
.O
..O
OOO
"""
        )
        assert results.data_rows.as_list() == [  # type:ignore
            [".", "O"],
            [".", ".", "O"],
            ["O", "O", "O"],
            [],
        ]

        results = PlainText._DATA_ROWS.parse_string(
            """\
........................O...........
......................O.O...........
............OO......OO............OO
...........O...O....OO............OO
OO........O.....O...OO..............
OO........O...O.OO....O.O...........
..........O.....O.......O...........
...........O...O....................
............OO......................"""
        )
        assert len(results.data_rows) == 9  # type:ignore
        assert results.data_rows[0].as_list()[24] == "O"  # type:ignore
        assert results.data_rows[6].as_list()[10] == "O"  # type:ignore
        assert results.data_rows[8].as_list()[11] == "."  # type:ignore
        assert results.data_rows[8].as_list()[12] == "O"  # type:ignore
        assert results.data_rows[8].as_list()[13] == "O"  # type:ignore
        assert results.data_rows[8].as_list()[14] == "."  # type:ignore

    def test_plain_text(self) -> None:
        """Test the PlainText file type."""
        with create_loader("../data/glider.cells") as loader:
            assert loader.__class__ is PlainText
            assert loader.metadata  # type: ignore
            assert loader.cells == [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
            assert (
                str(loader)
                == """\
PlainText
file: ../data/glider.cells
metadata: [['Name: Glider'], ['Author: Richard K. Guy'], ['The smallest, most common, and first discovered spaceship.'], ['www.conwaylife.com/wiki/index.php?title=Glider']]
cells:
. ■ .
. . ■
■ ■ ■"""
            )

    def test_empty_data_rows(self) -> None:
        """Test the PlainText file type."""
        with create_loader("../data/empty_data_rows.cells") as loader:
            assert loader.__class__ is PlainText
            assert loader.metadata == []  # type: ignore
            assert (
                str(loader)
                == """\
PlainText
file: ../data/empty_data_rows.cells
metadata: []
cells:
. . . . . . . . . . . . ■ ■
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
. . . . . ■ . . . . . . . .
. . ■ . . . . . . . . . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
. . . . . . . . . . . . . .
■ . . . . . . . . . . . . ."""
            )


# pylint: disable=protected-access
# pyright: reportPrivateUsage=false
class TestRunLengthEncoded:
    """Tests specifically for the class RunLengthEncoded."""

    def test_no_metadata(self) -> None:
        """Specific test for an RLE file with no metadata rows, and some other interesting things
        thrown in."""
        with create_loader("../data/no_metadata_test.rle") as loader:
            assert loader.metadata == []
            assert loader.cells == [
                (0, 1),
                (0, 3),
                (0, 5),
                (0, 7),
                (2, 2),
                (2, 3),
                (2, 4),
                (2, 5),
                (2, 6),
                (13, 0),
                (13, 1),
                (13, 2),
                (13, 7),
                (13, 8),
                (13, 9),
                (13, 10),
                (13, 11),
                (13, 12),
                (13, 13),
            ]

    def test_empty_row_data(self) -> None:
        """Specific test for testing data patterns like "7$" and "23$" which specifies a number of
        empty rows."""
        with create_loader("../data/t1point5infinitegrowth2.rle") as loader:
            # first two rows of data is (note "2$" at the end which skips a row of cells):
            #
            # 71b3o11b3o$70bo2bo10bo2bo$40b3o11b3o16bo4b3o6bo$40bo2bo10bo2bo15bo4bo
            # 2bo5bo$40bo6b3o4bo17bo4bo8bo$40bo5bo2bo4bo$41bo8bo4bo2$...
            # the skipped row is row index 7, so check it's all False
            assert loader.cells[43] == (6, 55)
            assert loader.cells[44] == (8, 72)
            assert len(loader.cells) == 1186

    def test_run_length_encoded(self) -> None:
        """Test the RunLengthEncoded file type."""
        # with create_loader("../data/Gosper_glider_gun.rle") as loader:
        with create_loader("../data/glider.rle") as loader:
            assert loader.__class__ is RunLengthEncoded
            assert loader.metadata  # type: ignore
            assert loader._cols  # type: ignore
            assert loader._rows  # type: ignore
            assert loader._rule  # type: ignore
            assert loader.cells == [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
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
            """\
#N next row has trailing space
#O 
#C
#
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""
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
        results: pp.ParseResults = RunLengthEncoded._METADATA_LINE.parse_string(
            """\
#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed c/4.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""
        )
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
        ).parse_string("x = 4, y = 5, rule = B3/S23")
        assert results.header.as_list() == [["x", 4], ["y", 5]]  # type:ignore
        assert results.rule.as_list() == ["B3/S23"]  # type:ignore

        results = (RunLengthEncoded._HEADER + RunLengthEncoded._RULE).parse_string(
            "x = 4, y = 5"
        )
        assert results.header.as_list() == [["x", 4], ["y", 5]]  # type:ignore
        assert len(results.rule) == 0  # type:ignore

    def test_data_rows_parser(self) -> None:
        """Test the CELL_ROWS parser."""
        results: pp.ParseResults = RunLengthEncoded._DATA_ROWS.parse_string(
            "bob$2bo$3o!"
        )
        assert results.data_rows.as_list() == [  # type:ignore
            ["b", "o", "b"],
            [2, "b", "o"],
            [3, "o"],
        ]

        results = RunLengthEncoded._DATA_ROWS.parse_string(
            """\
24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4b
obo$10bo5bo7bo$11bo3bo$12b2o!
"""
        )
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

        # Specific test for data that starts with multiple newlines
        results = RunLengthEncoded._DATA_ROWS.parse_string("32$8b3o$7bo3bo$6bo4b2o!")
        assert results.data_rows.as_list() == [  # type:ignore
            [32, "$"],
            [8, "b", 3, "o"],
            [7, "b", "o", 3, "b", "o"],
            [6, "b", "o", 4, "b", 2, "o"],
        ]
