"""File loader abstract class specifying the interface for loading cells from a file."""

from abc import ABC, abstractmethod
from types import TracebackType


class FileLoader(ABC):
    """ABC for the interface of different file encoding types for cells for Game of Life."""

    def __init__(self, file: str) -> None:
        """Initialise."""
        self._filename: str = file
        self.cells: list[list[bool]]
        self.metadata: list[list[int | bool]]

    @abstractmethod
    def __str__(self) -> str:
        """
        To str method default implementation.

        Sublasses might want to replace or augment this output.
        """
        # make a more human readable list of the cell values
        cells_str: str = "\n".join(
            [
                " ".join(["■" if cell else "." for cell in cell_row])
                for cell_row in self.cells
            ]
        )
        return (
            f"{type(self).__name__}\n"
            + f"file: {self._filename}\n"
            + f"metadata: {self.metadata}\n"
            + f"cells:\n{cells_str}"
        )

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
