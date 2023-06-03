"""Tests for all the FileLoader implementations."""

from pytest import raises
from gameoflife import create_loader, FileLoader, RunLengthEncoded


def test_create_loader() -> None:
    """Test the create_loader function."""
    loader: FileLoader = create_loader("", True)
    assert loader.__class__ is RunLengthEncoded
    with raises(ValueError):
        create_loader("", False)


def test_run_length_encoded() -> None:
    """Test the RunLengthEncoded file type."""
    with create_loader("../data/glider.rle", True) as loader:
        assert loader.cells()[0][0] is False
