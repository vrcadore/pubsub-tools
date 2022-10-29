import warnings
from datetime import timedelta
from typing import Generator

import wikipedia
from bs4 import GuessedAtParserWarning
from wikipedia.exceptions import DisambiguationError, PageError

warnings.simplefilter(action="ignore", category=GuessedAtParserWarning)


def get_random_summaries(num_iterations: int = -1) -> Generator[str, None, None]:
    """Return a generator of random wiki pages.

    Args:
        num_iterations (int, optional): Numeer of iterations. Defaults to -1.

    Returns:
        str: Return content of a random wiki page.

    Yields:
        Generator[str, None, None]: Generator
    """
    count = 0
    wikipedia.set_rate_limiting(False, min_wait=timedelta(milliseconds=20))

    while num_iterations < 0 or count < num_iterations:
        count = count + 1

        try:
            title = wikipedia.random()
            page = wikipedia.page(title=title)
            yield page.summary
        except (DisambiguationError, PageError):
            continue
