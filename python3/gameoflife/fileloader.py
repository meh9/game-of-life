"""File loader abstract class specifying the interface for loading cells from a file."""

from abc import ABC, abstractmethod
from types import TracebackType


class FileLoader(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    @abstractmethod
    def cells(self) -> list[list[bool]]:
        """Return an array of cells."""

    # TODO: add getting top-left coords, which will need new parsing too
    # Example: #R -22 -57
    # Gives the coordinates of the top-left corner of the pattern. RLE files produced by XLife
    # usually have this line, and the coordinates are usually negative, with the intention of
    # placing the centre of the pattern at the origin.


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
