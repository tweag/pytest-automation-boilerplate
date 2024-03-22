# pylint: disable=no-member
# pylint: disable=no-self-use
import string
import random
from datetime import datetime, timedelta

import structlog
from faker import Faker

logger = structlog.get_logger(__name__)


class DataUtils:
    def __init__(self):
        self._faker = Faker()

    def get_random_datetime(self, days=0, hours=1):
        logger.info("Generating random date time")
        current_datetime = datetime.utcnow().replace(
            minute=0, second=0, microsecond=0
        ) + timedelta(days=days, hours=hours)
        next_datetime_displayed = current_datetime.strftime(
            "Today" + " " + "%b %-d %-I:%M %p"
        )
        logger.info("Generated random date time is: ", next_datetime_displayed)
        return next_datetime_displayed

    def get_random_incomplete_password(self, length=7):
        logger.info("Generating random incomplete password")
        return self._faker.password(length)

    @staticmethod
    def get_random_text(source: str, length: int = 10):
        """Returns random string.
        Args:
            source: str - list of characters to choose from to generate a random string:
             alphabetic characters || numeric characters || alphabetic and numeric characters

            length: int - expected length of the generated random string. Default is 10
        """
        chars = None
        if source == "alphabetic characters":
            chars = string.ascii_letters
        elif source == "numeric characters":
            chars = string.digits
        elif source == "alphabetic and numeric characters":
            chars = string.ascii_letters + string.digits
        else:
            raise ValueError(f"Wrong source: {source}")

        return ''.join(random.SystemRandom().choices(chars, k=length))

    def get_random_email(self, domain):
        email = self._faker.email(domain=domain)
        return email
