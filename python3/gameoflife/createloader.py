"""
Simple function to create the different FileLoaders.

Using separate file to avoid module import issues.
"""

from gameoflife import FLContextManager, RunLengthEncoded


# TODO: it's terrible to pass each additional file type as a bool, must fix!
def create_loader(file: str, rle: bool | None) -> FLContextManager:
    """Create and return the correct FileLoader."""
    if rle:
        return RunLengthEncoded(file)
    raise ValueError("Incorrect or no file type specified.")
