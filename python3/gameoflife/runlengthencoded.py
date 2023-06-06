"""File Loader for Run Length Encoded file types."""

from io import TextIOWrapper
from types import TracebackType
from gameoflife import FileLoader, FLContextManager


class RunLengthEncoded(FLContextManager):
    """Implements loading Run Length Encoded data from files."""

    def __init__(self, file: str) -> None:
        """Initialise the loader."""
        self._filename: str = file
        self._file: TextIOWrapper

    def cells(self) -> list[list[bool]]:
        """Return an array of cells loaded from the file."""
        return [[False]]

    def __enter__(self) -> FileLoader:
        """Enter context manager."""
        self._file = open(self._filename, "r", encoding="UTF-8")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()
