"""
Simple function to create the different FileLoaders.

Using separate file to avoid module import issues.
"""
from .file_reader import FileReaderContextManager
from .runlengthencoded_reader import RunLengthEncodedReader
from .plaintext_reader import PlainTextReader


def create_reader(file: str) -> FileReaderContextManager:
    """Create and return the correct FileLoader."""
    match file.lower().split(".")[-1]:
        case "rle":
            return RunLengthEncodedReader(file)
        case "cells":
            return PlainTextReader(file)
        case other:
            raise ValueError(
                f"Can't tell what file type this is from its extension: '{other}', from {file}"
            )
    # circumvent pylint bug where it thinks create_reader() can return a not-ContextManager
    # just need to return a ContextManager here, even though the code can't be reached
    # see e.g.: https://github.com/pylint-dev/pylint/issues/5273
    return RunLengthEncodedReader("")
