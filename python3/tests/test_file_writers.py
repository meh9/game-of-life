"""Tests for all the FileWriter implementations."""

from os import stat, remove
from os.path import isfile
from time import time
from pytest import raises
from gameoflife.dataio.create_io import create_writer, create_reader
from gameoflife.dataio.file_writer import FileWriter
from gameoflife.dataio.plaintext_writer import PlainTextWriter
from gameoflife import Coordinate, GameOfLife, GameOfLifeSet


def test_create_writer() -> None:
    """Test the create_writer function."""
    writer: FileWriter = create_writer("test_file.cells")
    assert writer.__class__ is PlainTextWriter
    with raises(ValueError):
        create_writer("test_file.not_a_real_extension")


def test_write_gosper() -> None:
    """Test load and writing a Gosper glider gun."""
    _test_load_write("../data/Gosper_glider_gun.cells", 272)


def test_write_glider() -> None:
    """Test load and writing a Gosper glider gun."""
    _test_load_write("../data/glider.rle", 50)


def test_write_growth() -> None:
    """Test load and writing a Gosper glider gun."""
    _test_load_write("../data/t1point5infinitegrowth2.rle", 21617)


def _test_load_write(file_to_load: str, saved_file_size: int) -> None:
    """Test that we can save plaintext."""
    test_file_name: str = f"{time()}_test_file.cells"
    gol: GameOfLife = GameOfLifeSet()
    orig_cells: list[Coordinate]
    with create_reader(file_to_load) as reader:
        gol.add_cells(reader)
        orig_cells = gol.get_live_cells()
    with create_writer(test_file_name) as writer:
        writer.write(
            ["This is a comment.", "And another!", "!", ""], gol.get_live_cells()
        )
    assert isfile(test_file_name)
    assert stat(test_file_name).st_size == saved_file_size

    # test loading the saved data
    gol = GameOfLifeSet()
    with create_reader(test_file_name) as reader:
        gol.add_cells(reader)
    # Note that our PlainTextWriter writes the minimum it needs to, which can cause the written
    # data to be different from what we started with.
    # print(f"orig: {orig_cells}")
    # print(f"new:  {gol.get_live_cells()}")
    assert gol.get_live_cells() == orig_cells

    # if the test fails then cleanup doesn't happen and the file is left in the filesystem...
    remove(test_file_name)


def test_no_cells() -> None:
    """Test that we can save a game with no cells."""
    test_file_name: str = f"{time()}_test_file.cells"
    with create_writer(test_file_name) as writer:
        writer.write(["This is a comment.", "And another!", "!", ""], [])
    assert isfile(test_file_name)
    assert stat(test_file_name).st_size == 39
    # if the test fails then cleanup doesn't happen and the file is left in the filesystem...
    remove(test_file_name)
