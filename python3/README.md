# Let's do a Python version

[![codecov](https://codecov.io/gh/meh9/game-of-life/branch/main/graph/badge.svg?token=82OI1W6WTU)](https://codecov.io/gh/meh9/game-of-life)
[![build status](https://github.com/meh9/game-of-life/actions/workflows/python-app.yml/badge.svg)](https://github.com/meh9/game-of-life/actions/workflows/python-app.yml)

## Requirements

1. At least Python 3.10

(No testing has been carried out using Microsoft Windows. If someone does, please get in touch.)


## Installation

No real installation yet - currently run directly out of the source `python3` directory. You do need to install Python dependencies though, and it is recommended to use a `venv` as below.

The `venv` is best located in the root of the git directory in order for VSCode to pick it up automatically:

```
game-of-life % python3 -m venv .venv    
game-of-life % cd python3 
python3 % source ../.venv/bin/activate
(.venv) python3 % python3 -m venv .venv
(.venv) python3 % python3 -m pip install --upgrade pip
(.venv) python3 % pip install -r requirements.txt
```

## Developing

Things you might want to do when developing further (VSCode also does most of this):

1. `mypy --strict game_of_life.py gameoflife tests`
1. `black -v game_of_life.py gameoflife tests`
1. `python3 -m pytest -v --cov --cov-branch --cov-report html --cov-report term-missing`
1. TODO: pylint? pydocstyle? Currently VSCode takes care of this.


## Running

Simply run it from inside the `python3` directory:
```
python3 game_of_life.py
```

Or print out the command line help:
```
python3 game_of_life.py --help
```


## TODO:

Collecting a few things TODO in here in no particular order:
1. Show some form of Help "popup" showing all controls, any other info?
1. Python dependencies and transient dependencies license checker - possibility to check for license compatibility automatically?
1. Setup script? https://docs.python.org/3/distutils/setupscript.html
1. Use Sphinx with Google code guide: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
1. Configure pre-commit hooks for Mypy, Black, etc? https://composed.blog/python/pre-commit
1. (Done) Add ability to set the array size when using `--wrap`.
1. (Done) Test that array wrap of large patterns wrap correctly.
1. (Done) When loading data with `--wrap`, modulus all the coords with the width to "pack" in the cells in the available space.
1. (Done) Show x/y coords on screen (top left?)
1. (Done) Fix error loading `growing3c14piwaveship.rle`, looks like starting with `32$` is breaking parsing.
1. (Done) RunLengthEncoded or GameOfLifeDict is very memory hungry, see if we can do something about that.
1. (Done) Use argparse to parse command line args.
1. (Done) Add some kind of curses capability for displaying better in a terminal.
1. (Done) Use pytest to test things.
1. (Done) Don't forget your `requirements.txt` file.
1. (Done? VSCode does it. Not using Google standard though) Use Pylint to check code standard, use Google standard? https://www.pylint.org/ https://google.github.io/styleguide/pyguide.html
1. (Done) Use Mypy to check types.
1. (Done) Black as code formatting.

