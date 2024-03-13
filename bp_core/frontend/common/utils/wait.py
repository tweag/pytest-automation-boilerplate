import time
from typing import Callable

from bp_core.plugin import logger


def wait_until(
    func: Callable,
    *func_args,
    max_wait_time: int = 10,
    poll_frequency: int = 2,
    **func_kwargs
):
    end_time = time.time() + max_wait_time
    while True:
        try:
            value = func(*func_args, **func_kwargs)
            if value:
                return value
        except Exception:
            pass
        time.sleep(poll_frequency)
        if time.time() > end_time:
            logger.error(f"The element having locator '{func_args[0]}' is not visible")
            return False


def be_idle_for(seconds: int):
    time.sleep(seconds)
