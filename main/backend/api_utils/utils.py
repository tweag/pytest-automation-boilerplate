import json
from pathlib import Path
from typing import Dict

import requests

from main.backend.common.utils.custom_exceptions import InvalidFileFormatException, FileNotFoundException
from main.backend.common.utils.logger_config import logger

session = requests.Session()


def read_file(file_name: str) -> Dict:
    """Read the given file and return its content as a dictionary."""
    file_path = get_file_path(file_name)
    if not file_path.suffix == ".json":
        raise InvalidFileFormatException(f"Invalid file format '{file_path.suffix}'")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_file_path(file_name: str) -> Path:
    """Get the full path of the given file name."""
    file_path = Path("test_data/api/payloads") / file_name
    if not file_path.exists():
        raise FileNotFoundException(
            f"File '{file_name}' not found in '{file_path.parent}'"
        )
    return file_path


def make_request(
    method: str, api_endpoint: str, headers: Dict = None, payload: Dict = None
) -> requests.Response:
    """Make a request using the given method and log the request & response details."""
    response = session.request(method, api_endpoint, headers=headers, json=payload)
    log_details = "\n".join(
        [
            f"Request Method: {method.upper()}",
            f"Request URI: {api_endpoint}",
            f"Request Headers: {headers}",
            f"Request Payload: {payload}",
            f"Response Status Code: {response.status_code}",
            f"Response Headers: {response.headers}",
            f"Response Body: {response.json()}",
        ]
    )
    logger.debug(log_details)
    return response


def get_request(api_endpoint: str = None, headers: Dict = None) -> requests.Response:
    """Make a GET request."""
    return make_request("GET", api_endpoint=api_endpoint, headers=headers)


def post_request(
    api_endpoint: str = None, headers: Dict = None, payload: Dict = None
) -> requests.Response:
    """Make a POST request."""
    return make_request(
        "POST", api_endpoint=api_endpoint, headers=headers, payload=payload
    )


def put_request(
    api_endpoint: str = None, headers: Dict = None, payload: Dict = None
) -> requests.Response:
    """Make a PUT request."""
    return make_request(
        "PUT", api_endpoint=api_endpoint, headers=headers, payload=payload
    )


def delete_request(api_endpoint: str = None, headers: Dict = None) -> requests.Response:
    """Make a DELETE request."""
    return make_request("DELETE", api_endpoint=api_endpoint, headers=headers)
