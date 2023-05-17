"""Game of Life abstract class specifying the interface."""

from abc import ABC, abstractmethod


class GameOfLife(ABC):
    """Abstract class to specify the interface for different implementations of Game of Life."""

    @abstractmethod
    def __str__(self) -> str:
        """Produce a human readable string to represent the state of the GoL universe."""

    @abstractmethod
    def progress(self) -> None:
        """Progress another generation."""

    @abstractmethod
    def set_cell(self, row: int, col: int, live: bool) -> None:
        """Set a cell in the universe to the given live value."""

    @abstractmethod
    def count_live_cells(self) -> int:
        """Count the total number of live cells in the GoL universe."""

    @abstractmethod
    def get_cell(self, row: int, col: int) -> bool:
        """Return the live status of the given cell."""
