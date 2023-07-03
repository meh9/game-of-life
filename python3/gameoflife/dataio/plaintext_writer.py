"""File Writer for Plain Text file types."""

from io import TextIOWrapper
from types import TracebackType
from .file_writer import FileWriter, FileWriterContextManager


# pylint: disable=pointless-string-statement
""" 
!Name: Glider
!Author: Richard K. Guy
!The smallest, most common, and first discovered spaceship.
!www.conwaylife.com/wiki/index.php?title=Glider
.O
..O
OOO
"""


class PlainTextWriter(FileWriterContextManager):
    """Implements writing Plain Text data to files."""

    def __init__(self, file: str) -> None:
        """Initialise the reader."""
        super().__init__(file)
        self._file: TextIOWrapper

    def __enter__(self) -> FileWriter:
        """Enter context manager which causes the file to be parsed immediately."""
        self._file = open(self._filename, "w", encoding="UTF-8")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self._file.close()
