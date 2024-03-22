import os
from pathlib import Path
from typing import Union
from dotenv import load_dotenv
from main.utils.singleton import SingletonMeta


def load_env_from_local_dotenv_file(
    dotenv_file_path: Union[str, None] = None
):
    """Function to load environment variables from `.local.env` file

    Args:
        dotenv_file_path: str | None (Default) - Absolute Path of the .local.env file.

    Returns:
        None
    """
    if dotenv_file_path is None:
        dotenv_file = Path(__file__ + "/../../../env_configs/.local.env").resolve()
    else:
        dotenv_file = Path(dotenv_file_path).resolve()

    if dotenv_file.is_file():
        load_dotenv(dotenv_path=dotenv_file, verbose=True)


class EnvVariables(metaclass=SingletonMeta):
    def __init__(
        self,
        local_dotenv_file_path: Union[str, None] = None,
    ) -> None:
        self.env = local_dotenv_file_path
        load_env_from_local_dotenv_file(self.env)


    @property
    def base_url(self):
        return os.getenv("BASE_URL", "")

    @property
    def basic_auth_username(self):
        return os.getenv("BASIC_AUTH_USERNAME", "")

    @property
    def basic_auth_password(self):
        return os.getenv("BASIC_AUTH_PASSWORD", "")

    @property
    def login_username(self):
        return os.getenv("LOGIN_USERNAME", "")

    @property
    def login_password(self):
        return os.getenv("LOGIN_PASSWORD", "")

    def get(self, var_name, default=None) -> str:
        return os.getenv(var_name, default)
