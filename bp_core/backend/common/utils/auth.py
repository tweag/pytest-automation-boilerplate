"""auth.py

Module for Custom Authentication Methods
"""
from requests import auth

__all__ = ["HTTPBearerAuth"]


class HTTPBearerAuth(auth.AuthBase):
    """Simple Implementation of Bearer Authentication Model

    Attributes
    ----------
    `bearer_token: str`

    Methods
    -------
    None
    """

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    def __repr__(self):
        return "HTTPBearerAuth(bearer_token=*CENSORED*)"

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.bearer_token}"
        return request
