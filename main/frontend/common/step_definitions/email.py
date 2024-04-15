import base64
import json
import os
import re
import time

import pytest
import structlog
from bs4 import BeautifulSoup
from collections import defaultdict

from main.utils.email_reader import create_json

PROJECT_DIR = os.getcwd()
test_data_dir = os.path.join(PROJECT_DIR, "test_data/files/email_data.json")

from pytest_bdd import parsers, when, then
from main.frontend.common.helpers.selenium_generics import SeleniumGenerics

logger = structlog.get_logger(__name__)
pytest.globalDict = defaultdict()


@when(parsers.re("I get about link from email '(?P<user_type>.*)'"),
      converters=dict(user_type=str))
@then(parsers.re("I get about link from email '(?P<user_type>.*)'"),
      converters=dict(user_type=str))
def check_email(user_type, selenium_generics: SeleniumGenerics):
    time.sleep(5)
    create_json()
    from datetime import date
    today = date.today()
    from datetime import timedelta

    yesterday = today - timedelta(days=1)
    date_today = today.strftime("%d %b %Y")
    date_yesterday = yesterday.strftime("%d %b %Y")
    if '0' in date_today[0]:
        date_today = date_today[1:]
    f = open(test_data_dir)
    data = json.load(f)
    for i in data:
        value = i
        if "Test Project Data" in value["Subject"] or "Test Data" in value["Subject"] and \
                "tauqirsarwar1@gmail.com" in value["From"] and date_today in value["Date"] or \
                date_yesterday in value["Date"] and user_type in value["To"]:
            decoded_data = base64.b64decode(value["Message"])
            soup = BeautifulSoup(decoded_data, "lxml")
            email_body = str(soup.body()[0])
            url = re.findall('https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*, ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             email_body)
            final_url = ""
            if len(url) >= 1:
                final_url = str(url[0]).replace('amp;', '')
            if len(url) == 0:
                decoded_data = base64.b64decode(value["Url"])
                soup = BeautifulSoup(decoded_data, "lxml")
                email_body = str(soup.body()[0])
                url = re.findall('https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*, ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                 email_body)
                new_url = ''
                for j in url:
                    if 'Test Project Data' in j or 'Test Data' in j:
                        new_url = j
                final_url = str(new_url).replace('amp;', '')
                pytest.globalDict['final_url'] = final_url
            selenium_generics.navigate_to_url(final_url)

            break
    f.close()


@then('I reopen the email link')
def reopen_final_url(selenium_generics: SeleniumGenerics):
        final_url = pytest.globalDict['final_url']
        selenium_generics.navigate_to_url(final_url)
