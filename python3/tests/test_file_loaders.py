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


def test_create_loader() -> None:
    """Test the create_loader function."""
    loader: FileLoader = create_loader("")
    # the below will change if and when we support different loader types
    assert loader.__class__ is RunLengthEncoded
    # with raises(ValueError):
    #     create_loader("")


def test_run_length_encoded() -> None:
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
            == "[['N', 'Glider'], ['O', 'Richard K. Guy'], ['C', 'The smallest, most common, and "
            + "first discovered spaceship. Diagonal, has period 4 and speed c/4.'], ['C', "
            + "'www.conwaylife.com/wiki/index.php?title=Glider']]\ncols: 3, rows: 3, rule: B3/S23"
        )


class TestRunLengthEncoded:
    """Tests specifically for the class RunLengthEncoded."""

    def test_metadata_parser(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = pp.ZeroOrMore(
            RunLengthEncoded.METADATA_LINE
        ).parse_string(GLIDER)
        assert len(results) == 8
        assert results[0] == "N"
        assert results[1] == "Glider"
        assert results[-1] == "www.conwaylife.com/wiki/index.php?title=Glider"
        assert results.metadata[1][1] == "Richard K. Guy"  # type: ignore

    def test_header_rule_parser(self) -> None:
        """Test the HEADER parser."""
        results: pp.ParseResults = (
            RunLengthEncoded.HEADER + RunLengthEncoded.RULE
        ).parse_string(HEADER_RULE)
        assert results.header[0][1] == 4  # type:ignore
        assert results.header[1][1] == 5  # type:ignore
        assert results.rule[1] == "B3/S23"  # type:ignore

        results = (RunLengthEncoded.HEADER + RunLengthEncoded.RULE).parse_string(
            HEADER_NO_RULE
        )
        assert results.header[0][1] == 4  # type:ignore
        assert results.header[1][1] == 5  # type:ignore
        assert len(results.rule) == 0  # type:ignore
