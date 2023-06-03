"""File loader abstract class specifying the interface for loading cells from a file."""

from abc import ABC, abstractmethod
from types import TracebackType


class FileLoader(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    @abstractmethod
    def cells(self) -> list[list[bool]]:
        """Return an array of cells."""


class FLContextManager(FileLoader):
    """ABC for adding context management to FileLoaders."""

    @abstractmethod
    def __enter__(self) -> FileLoader:
        """Enter context manager."""

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
