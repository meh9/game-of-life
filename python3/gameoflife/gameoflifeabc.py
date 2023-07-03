"""Game of Life abstract class specifying the interface."""

from abc import ABC, abstractmethod
from gameoflife.dataio.filereader import FileReader
from .coordinate import Coordinate


class GameOfLife(ABC):
    """Abstract class to specify the interface for different implementations of Game of Life."""

    def __init__(self) -> None:
        """Initialise."""
        self._generation: int = 0

    @abstractmethod
    def __str__(self) -> str:
        """Produce a human readable string to represent the state of the GoL universe."""

    @abstractmethod
    def progress(self) -> int:
        """Progress another generation, return the number of live cells in the new generation."""

    @abstractmethod
    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the universe to the given live value."""

    @abstractmethod
    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""

    @abstractmethod
    def get_cell(self, row: int, col: int) -> bool | None:
        """Return the live status of the given cell."""

    @property
    def generation(self) -> int:
        """Return the current generation of the game."""
        return self._generation

    @generation.setter
    def generation(self, gen: int) -> None:
        """Return the current generation of the game."""
        self._generation = gen

    def add_cells(self, loader: FileReader) -> None:
        """Load cells from the given loader."""
        for row, col in loader.cells:
            self.set_cell(row, col, True)

    @abstractmethod
    def get_live_cells(self) -> list[Coordinate]:
        """
        Return a list of the Coordinates of all the live cells.

        The list must be sorted by row top to bottom and then in the row from left to right.
        """
