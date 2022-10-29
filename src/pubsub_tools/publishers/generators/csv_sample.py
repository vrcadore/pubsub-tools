import json
import time
from typing import Generator

import pandas as pd


def get_csv_sample(
    filepath: str,
    msg_format: str = "csv",
    num_iterations: int = -1,
    sleep_ms: int = 100,
) -> Generator[str, None, None]:
    """Return a generator of random rows from a csv.

    Args:
        filepath (str): Numeer of iterations.
        msg_format (str, optional): Numeer of iterations. Defaults to csv.
        num_iterations (int, optional): Number of iterations. Defaults to -1.
        sleep_ms (int, optional): Time to wait after message(ms). Defaults to 100.

    Returns:
        str: Return content of a random wiki page.

    Yields:
        Generator[str, None, None]: Generator
    """

    df = pd.read_csv(filepath)

    count = 0
    while num_iterations < 0 or count < num_iterations:
        count = count + 1

        sample = df.sample()
        if msg_format == "dict":
            message = json.dumps(sample.to_dict())
        elif msg_format == "csv":
            message = ",".join(sample.astype(str).iloc[0].to_list())
        else:
            message = " ".join(sample.astype(str).iloc[0].to_list())

        yield message

        if sleep_ms > 0:
            # Sleep for a while
            time.sleep(sleep_ms / 1000)
