# Let's do a Python version

Collecting a few things TODO in here in no particular order:
1. Setup script? https://docs.python.org/3/distutils/setupscript.html
1. Use Sphinx with Google code guide: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
1. Use argparse to parse command line args: https://docs.python.org/3/library/argparse.html
1. Add some kind of curses capability for displaying better in a terminal. Maybe console? https://mixmastamyk.bitbucket.io/console/
1. Configure pre-commit hooks for Mypy, Black, etc? https://composed.blog/python/pre-commit
1. (Done) Use pytest to test things (unittest?): https://docs.pytest.org/en/stable/ https://docs.python.org/3/library/unittest.html
1. (Done) Don't forget your `requirements.txt` file.
1. (Done? VSCode does it. Not using Google standard though) Use Pylint to check code standard, use Google standard? https://www.pylint.org/ https://google.github.io/styleguide/pyguide.html
1. (Done? VSCode does it) Use Mypy to check types: https://mypy-lang.org/
1. (Done? VSCode does it) Black as code formatting? https://github.com/psf/black


## Manual steps
1. `pip install -r requirements.txt`
1. `mypy --strict *.py`
1. `black *.py`
1. `pytest -v`
1. `python3 game_of_life.py`
1. pylint? pydocstyle?
