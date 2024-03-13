# pylint: disable=import-outside-toplevel
# pylint: disable=no-member
import base64
import errno
import json
import math
import os
import random
import re
import shutil
import string
import time
from collections import namedtuple
from datetime import datetime
from functools import reduce
from os import path, strerror
from pathlib import Path
from typing import Callable, List

import structlog

logger = structlog.get_logger(__name__)

OutputDirs = namedtuple(
    "OutputDirs",
    "vis_base vis_test vis_diff run_logs reports downloads screenshots",
)

TEMP_SCREENSHOTS = "output/temp_screenshots/"


def initialize_output_dirs():
    output_dir = Path(__file__ + "/../../../output/").resolve()
    directories = OutputDirs(
        output_dir / "visualtesting" / "base",
        output_dir / "visualtesting" / "test",
        output_dir / "visualtesting" / "diff",
        output_dir / "run_logs",
        output_dir / "reports",
        output_dir / "downloads",
        output_dir / "screenshots",
    )

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True)
    return directories


def read_file(file_name):
    logger.info("Started reading file", file_name)
    file_path = get_file_path(file_name)
    with open(file_path, encoding="utf-8") as fl:
        extension = path.splitext(file_path)[1]
        if extension == ".json":
            raw_data = json.load(fl)
            return raw_data
        if extension == ".txt":
            raw_data = fl.read()
            return raw_data
        raise extension
    logger.info("Completed reading the file: ", file_name)


def get_file_path(file_name):
    path_object = Path(file_name)
    if not path_object.exists():
        logger.error("File: %s not found", str(file_name))
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), file_name)
    return path_object.resolve()


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def deep_get(dictionary, *keys):
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)


class Waiter:
    def __init__(
        self,
        timeout: int = 5,
        poll_interval: float = 1,
        raise_error_on_failure: bool = False,
        error_message: str = None,
    ):
        self._timeout: int = timeout
        self._poll_interval: float = poll_interval
        self._throw_error: bool = raise_error_on_failure
        self._error_msg: str = error_message

    """Waits for the predicate to return true. Timeout, poll interval, etc, are set via other methods"""

    def wait_for(self, predicate):
        start_time = time.time()
        is_success = False
        last_error = None

        while not is_success:
            time.sleep(self._poll_interval)

            try:
                logger.debug("Checking predicate")
                is_success = predicate()
            except Exception as e:
                last_error = e

            elapsed_time = time.time() - start_time
            if not is_success and elapsed_time >= self._timeout:
                logger.debug(f"Wait failed after {elapsed_time} seconds")
                self.throw_error_if_the_case(last_error)
                break

    def throw_error_if_the_case(self, last_error):
        if self._throw_error:
            if self._error_msg:
                raise ValueError(self._error_msg)
            raise last_error if last_error else Exception()


class Retry:
    def __init__(
        self,
        limit: int = 2,
        retry_interval: int = 1,
        raise_error_on_failure: bool = False,
        error_message: str = None,
    ):
        self._limit: int = limit
        self._retry_interval: float = retry_interval
        self._throw_error: bool = raise_error_on_failure
        self._error_msg: str = error_message
        self._operation: Callable = None

    def action(self, operation: Callable):
        self._operation = operation
        return self

    def till_success_of(self, predicate):
        """Retries the operation until it succeeds or the retry limit is reached.
        The limit, retry interval, etc, are set via other methods"""
        count = 0
        is_failure = True
        last_error = None

        while count < self._limit and is_failure:
            try:
                self._operation()
                is_failure = not predicate()
            except Exception as e:
                last_error = e

            count += 1
            time.sleep(self._retry_interval)

        if self._throw_error and is_failure:
            logger.debug(f"Retry failed after {count} tries")
            if self._error_msg:
                raise ValueError(self._error_msg)
            raise last_error


def get_random_string(size: int, no_digits: bool = False):
    chars = string.ascii_letters if no_digits else string.ascii_letters + string.digits
    return "".join(random.SystemRandom().choices(chars, k=size))


def get_random_bool():
    return random.SystemRandom().choice([True, False])


def get_datetime_string():
    return f"{datetime.now():%Y-%m-%d %H-%M-%S}"


def get_date_string():
    return f"{datetime.now():%Y-%m-%d}"


def get_random_int(end: int, start: int = 0):
    return random.SystemRandom().randint(start, end)


def remove_chars_from_string(input_str: str, chars: List):
    return input_str.translate({ord(x): '' for x in chars})


def zip_screenshots_files(source_folder, destination_file_name, destination_folder):
    if not os.path.exists(source_folder):
        return ""
    output = shutil.make_archive(
        base_name=destination_file_name,
        format="zip",
        root_dir=os.path.abspath(source_folder)
    )
    shutil.move(output, destination_folder)
    return output


def save_base64_as_png(data, dest_folder, dest_file_name):
    os.makedirs(os.path.join(dest_folder), exist_ok=True)
    png_file = base64.b64decode(data)
    with open(dest_folder / f"{dest_file_name}", "wb") as file:
        file.write(png_file)


def remote_execute_cmd_commands(driver, cmd, params=None):
    if params is None:
        params = {}
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def remove_multiple_spaces(text: str):
    return re.sub(' +', ' ', text)
