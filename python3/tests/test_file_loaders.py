"""Tests for all the FileLoader implementations."""

# from pytest import raises
from gameoflife import create_loader, FileLoader, RunLengthEncoded
from gameoflife import runlengthencoded
import pyparsing as pp

GLIDER: str = """\
#N Glider
#O Richard K. Guy
#C The smallest, most common, and first discovered spaceship. Diagonal, has period 4 and speed c/4.
#C www.conwaylife.com/wiki/index.php?title=Glider
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
"""


def test_create_loader() -> None:
    """Test the create_loader function."""
    loader: FileLoader = create_loader("")
    assert loader.__class__ is RunLengthEncoded
    # with raises(ValueError):
    #     create_loader("")


def test_run_length_encoded() -> None:
    """Test the RunLengthEncoded file type."""
    with create_loader("../data/glider.rle") as loader:
        assert loader.cells()[0][0] is False


class TestRunLengthEncoded:
    """Tests specifically for the class RunLengthEncoded."""

    def test_metadata_parser(self) -> None:
        """Test the METADATA parser."""
        results: pp.ParseResults = runlengthencoded.METADATA.parse_string(GLIDER)
        assert len(results) == 2  # N Glider
        assert results[0] == "N"
        assert results[1] == "Glider"
