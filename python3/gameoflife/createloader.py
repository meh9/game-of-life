"""
Simple function to create the different FileLoaders.

Using separate file to avoid module import issues.
"""

from gameoflife import FLContextManager
from gameoflife.dataloaders import RunLengthEncoded


# TODO: did all this prematurely - we don't have different loaders yet!
def create_loader(file: str) -> FLContextManager:
    """Create and return the correct FileLoader."""
    # if rle:
    return RunLengthEncoded(file)
    # raise ValueError("Incorrect or no file type specified.")
