"""Base session"""

import time
from json.decoder import JSONDecodeError
from os import environ
from pathlib import Path
from typing import Union

import requests
import structlog

from . import __version__
from ._enums import METHODS
from ._exception import StatusCodeError, TestRailError

LOGGER = structlog.get_logger(__package__)

RATE_LIMIT_TIMEOUT = 3
RATE_LIMIT_STATUS_CODE = 429

class Session:
    """Base Session"""

    _user_agent = "Python TestRail API v: {}".format(__version__)

    def __init__(
        self, config, exc: bool = False, rate_limit: bool = True, **kwargs
    ) -> None:
        """
        :param url:
            TestRail address
        :param email:
            Email for the account on the TestRail
        :param password:
            Password for the account on the TestRail
        :param exc:
            Catching exceptions
        :param kwargs:
            :key timeout: int (default: 30)
            :key verify: bool (default: True)
            :key headers: dict
        """
        _url = (
            config.getoption("--testrail-url")
            or config.inicfg.get("testrail-url")
            or environ.get("TESTRAIL_URL")
        )
        _email = (
            config.getoption("--testrail-email")
            or config.inicfg.get("testrail-email")
            or environ.get("TESTRAIL_EMAIL")
        )
        _key = (
            config.getoption("--testrail-key")
            or config.inicfg.get("testrail-key")
            or environ.get("TESTRAIL_KEY")
        )
        if not _url or not _email or not _key:
            raise TestRailError("No url or email or key values set. Aborting!!!")
        if _url.endswith("/"):
            _url = _url[:-1]
        self.__base_url = "{}/index.php?/api/v2/".format(_url)
        self.__user_email = _email
        self.__timeout = kwargs.get("timeout", 30)
        self.__session = requests.Session()
        self.__session.headers["User-Agent"] = self._user_agent
        self.__session.headers.update(kwargs.get("headers", {}))
        self.__session.verify = kwargs.get("verify", True)
        self.__session.auth = (self.__user_email, _key)
        self.__exc = exc
        self._rate_limit = rate_limit
        LOGGER.info(
            "Create Session{url: %s, user: %s, timeout: %s, headers: %s, verify: "
            "%s, exception: %s}",
            _url,
            self.__user_email,
            self.__timeout,
            self.__session.headers,
            self.__session.verify,
            self.__exc,
        )

    @property
    def user_email(self) -> str:
        """Get user email"""
        return self.__user_email

    def __response(self, response: requests.Response):
        if not response.ok:
            LOGGER.error(
                "Code: %s, reason: %s url: %s, content: %s",
                response.status_code,
                response.reason,
                response.url,
                response.content,
            )
            if not self.__exc:
                raise StatusCodeError(
                    response.status_code,
                    response.reason,
                    response.url,
                    response.content,
                )

        LOGGER.debug("Response body: %s", response.text)
        try:
            return response.json()
        except ValueError:
            return response.text or None

    def request(self, method: METHODS, src: str, raw: bool = False, **kwargs):
        """Base request method"""
        url = "{}{}".format(self.__base_url, src)
        if not src.startswith("add_attachment"):
            headers = kwargs.setdefault("headers", {})
            headers.update({"Content-Type": "application/json"})

        if "params" in kwargs:
            for key, value in kwargs["params"].items():
                if isinstance(value, list):
                    kwargs["params"][key] = ",".join([str(i) for i in value])




        iterations = 3
        for count in range(iterations):
            try:
                response = self.__session.request(
                    method=method.value, url=url, timeout=self.__timeout, **kwargs
                )
            except Exception as err:
                LOGGER.error("%s", err, exc_info=True)
                raise
            if (
                self._rate_limit
                and response.status_code == RATE_LIMIT_STATUS_CODE
                and count < iterations - 1
            ):
                time.sleep(int(response.headers.get("retry-after", RATE_LIMIT_TIMEOUT)))
                continue
            # LOGGER.info("Response header: %s", response.headers)
            return response if raw else self.__response(response)

    @staticmethod
    def _path(path: Union[Path, str]) -> Path:
        return path if isinstance(path, Path) else Path(path)

    def attachment_request(
        self, method: METHODS, src: str, file: Union[Path, str], **kwargs
    ):
        """Send attach"""
        file_attachment = self._path(file)
        with file_attachment.open("rb") as attachment:
            return self.request(method, src, files={"attachment": attachment}, **kwargs)

    def get_attachment(
        self, method: METHODS, src: str, file: Union[Path, str], **kwargs
    ) -> Path:
        """Downloads attach"""
        file_attachment = self._path(file)
        response = self.request(method, src, raw=True, **kwargs)
        if response.ok:
            with file_attachment.open("wb") as attachment:
                attachment.write(response.content)
            return file_attachment
        return self.__response(response)
