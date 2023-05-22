"""Import all the other sources and re-export them for easier importing elsewhere."""

# pylint: disable=useless-import-alias
from gameoflife.gameoflifeabc import GameOfLife as GameOfLife
from gameoflife.gameoflifearrays import GameOfLifeArrays as GameOfLifeArrays
from gameoflife.gameoflifesorteddict import GameOfLifeSortedDict as GameOfLifeSortedDict
from gameoflife.main import MainGame as MainGame
