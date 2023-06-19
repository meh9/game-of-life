"""Import all the other sources and re-export them for easier importing elsewhere."""

# pylint: disable=useless-import-alias
from gameoflife.fileloader import FileLoader as FileLoader
from gameoflife.fileloader import FLContextManager as FLContextManager
from gameoflife.createloader import create_loader as create_loader
from gameoflife.gameoflifeabc import GameOfLife as GameOfLife
from gameoflife.gameoflifearrays import GameOfLifeArrays as GameOfLifeArrays
from gameoflife.gameoflifedict import GameOfLifeDict as GameOfLifeDict
from gameoflife.gameoflifeset import GameOfLifeSet as GameOfLifeSet
from gameoflife.main import MainGame as MainGame
