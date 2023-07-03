"""Tests for all the FileWriter implementations."""

from pytest import raises
from gameoflife.dataio.create_io import create_writer
from gameoflife.dataio.file_writer import FileWriter
from gameoflife.dataio.plaintext_writer import PlainTextWriter


def test_create_writer() -> None:
    """Test the create_writer function."""
    writer: FileWriter = create_writer("file.cells")
    assert writer.__class__ is PlainTextWriter
    with raises(ValueError):
        create_writer("foo.bar")
