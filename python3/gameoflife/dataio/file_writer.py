"""File writer abstract class specifying the interface for writing cells to a file."""

from abc import ABC, abstractmethod
from types import TracebackType
from gameoflife import Coordinate


class FileWriter(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    def __init__(self, file: str) -> None:
        """Initialise."""
        self._filename: str = file

    @abstractmethod
    def write(self, metadata: list[str], cells: list[Coordinate]) -> None:
        """Write the Game of Life data to the file."""


class FileWriterContextManager(FileWriter):
    """ABC for adding context management to FileReaders."""

    @abstractmethod
    def __enter__(self) -> FileWriter:
        """Enter context manager."""

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
