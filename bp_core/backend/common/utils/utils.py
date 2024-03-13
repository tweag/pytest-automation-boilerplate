"""utils.py

Utility to parse api test data json file
"""
import json
from collections import namedtuple
from pathlib import Path
from typing import Tuple
from bp_core.utils import env_variables

Dataset = namedtuple("Dataset", "request_args set_env")

json_python_obj_map = {
    "object": dict,
    "array": list,
    "string": str,
    "number (int)": int,
    "number (real)": float,
    "true": True,
    "false": False,
    "null": None,
}


def urlappend(current_url: str, *incoming_portions: Tuple[str]) -> str:
    """urlappend - simple url appender - not so smart

    Simple url appender function to append portions of url by adding two portions
    by correcting the / sign. For the last portion of the url, we would stick with
    the backslash if provided in the input.

    This function is to be used in two cases:
    * Adding endpoint to base url
    * Adding url parameters

    This is not to be used for query parameters.

    Arguments
    ---------
    current_url : str
        existing url
    incoming_portions : Tuple[str]
        portions of url that has to be appended to existing url in order

    Returns
    -------
    str
        Appended whole url
    """

    current_url = current_url.rstrip("/")
    incoming_portions = [
        incoming_portion.strip("/")
        if _ != len(incoming_portions) - 1
        else incoming_portion.lstrip("/")
        for _, incoming_portion in enumerate(list(incoming_portions))
    ]
    return "/".join([current_url] + incoming_portions)


def load_json_file(file_path: str):
    """load_file

    Arguments
    ---------
    `file_path: Path`

    Returns
    -------
    Key-Value pairs of loaded json file

    Raises
    ------
    `json.JSONDecodeError`
    """
    with open(Path(file_path), "r", encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from {file_path}: {str(e)}")
            raise
