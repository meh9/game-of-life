"""Import all the other sources and re-export them for easier importing elsewhere."""

# pylint: disable=useless-import-alias
from gameoflife.coordinate import Coordinate as Coordinate
from gameoflife.gol_abc import GameOfLife as GameOfLife
from gameoflife.gol_arrays import GameOfLifeArrays as GameOfLifeArrays
from gameoflife.gol_dict import GameOfLifeDict as GameOfLifeDict
from gameoflife.gol_set import GameOfLifeSet as GameOfLifeSet
from gameoflife.main import MainGame as MainGame
