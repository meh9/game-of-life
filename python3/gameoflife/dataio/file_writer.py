"""File writer abstract class specifying the interface for writing cells to a file."""

from abc import ABC, abstractmethod
from types import TracebackType


class FileWriter(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    def __init__(self, file: str) -> None:
        """Initialise."""
        self._filename: str = file

    def __str__(self) -> str:
        """
        To str method default implementation.

        Sublasses might want to replace or augment this output.

        WARNING: for large patterns this will run out of memory as it tries to print a matrix.
        """
        raise NotImplementedError


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
