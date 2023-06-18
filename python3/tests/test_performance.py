"""Performance tests for all the Conway's Game of Life implementations."""

import logging
from time import perf_counter_ns
import pytest
from gameoflife import GameOfLife, GameOfLifeDict, create_loader

pytestmark: pytest.MarkDecorator = pytest.mark.performance
LOGGER: logging.Logger = logging.getLogger(__name__)


def test_dict_progress_large_file() -> None:
    """Performance test goes here."""
    gol: GameOfLife = GameOfLifeDict()
    start: int = perf_counter_ns()
    with create_loader("../data/period59glidergun.rle") as loader:
        gol.add_cells(loader)
    last_gen_time: int = perf_counter_ns() - start
    LOGGER.info(
        "'create_loader('period59glidergun.rle')' time: %s µs",
        round(last_gen_time / 1000),
    )

    # measure the progress() method
    times: int = 10
    start = perf_counter_ns()
    for _ in range(times):
        gol.progress()
    last_gen_time = perf_counter_ns() - start
    LOGGER.info(
        "'gol.progress()' average(%s) time: %s µs",
        times,
        round(last_gen_time / 1000 / times),
    )
