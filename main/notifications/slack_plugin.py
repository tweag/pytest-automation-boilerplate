import os
import time
from collections import defaultdict
from datetime import timedelta
from enum import Enum
from typing import Dict, List, Optional

import requests
from _pytest.config import Config
from _pytest.config.argparsing import Parser


class Outcome(str, Enum):
    FAILED = 'failed'
    PASSED = 'passed'
    SKIPPED = 'skipped'


class SlackPlugin:
    """
    Slack plugin for pytest

    Reports test results to Slack via an Incoming Webook integration.

    Enable by adding `pytest_plugins = ['module.path.to.slack_plugin']` to `conftest.py`, and by setting
    the webhook URL argument or environment variable.
    """

    def __init__(
            self,
            webhook_url: str,
            channel: str,
            results_url: Optional[str] = None,
            failure_only: Optional[bool] = False,
    ):
        self.webhook_url = webhook_url
        self.channel = channel
        self.results_url = results_url
        self.failure_only = failure_only

        self.reports: Dict[Outcome, List] = defaultdict(list)
        self.session_start = 0
        self.session_end = 0

    @staticmethod
    def format_duration(duration: timedelta, *, abbrev: bool = False) -> str:
        total_seconds = int(duration.total_seconds())
        periods = [
            ('hour', 'h', 3600),
            ('minute', 'm', 60),
            ('second', 's', 1)
        ]

        strings = []
        for unit_name, unit_abbrev, unit_size in periods:
            unit = unit_abbrev if abbrev else unit_name
            if total_seconds > unit_size:
                period_value, total_seconds = divmod(total_seconds, unit_size)
                if abbrev:
                    strings.append(f'{period_value}{unit}')
                else:
                    plural = 's' if period_value != 1 else ''
                    strings.append(f'{period_value} {unit}{plural}')

        return ' '.join(strings)

    @property
    def session_duration(self) -> timedelta:
        return timedelta(seconds=self.session_end - self.session_start)

    @property
    def passed_tests_count(self) -> int:
        return len(self.reports[Outcome.PASSED])

    @property
    def skipped_tests_count(self) -> int:
        return len(self.reports[Outcome.SKIPPED])

    @property
    def failed_tests_count(self) -> int:
        return len(self.reports[Outcome.FAILED])

    @property
    def total_tests_count(self) -> int:
        return sum(len(outcome) for outcome in self.reports.values())

    @property
    def report_summary(self) -> str:
        return (
            f'*{self.passed_tests_count} passed,* '
            f'*{self.failed_tests_count} failed,* '
            f'{self.skipped_tests_count} skipped '
            f'({self.total_tests_count} total) '
            f'in {self.format_duration(duration=self.session_duration, abbrev=True)}'
        )

    @property
    def failed_test_names(self) -> List[str]:
        test_names = []
        for r in self.reports[Outcome.FAILED]:
            if hasattr(r, 'scenario') is False:
                test_name = r.test_name[0]
            else:
                test_name = r.scenario['name']

            if r.when in ('setup', 'teardown'):
                test_name += f' (during {r.when})'
            test_names.append(test_name)
        return sorted(test_names)

    def create_message(self) -> dict:
        message = {
            'username': 'pytest',
            'icon_url': 'https://docs.pytest.org/en/latest/_static/favicon.png',
            'text': f'Test Execution Results: {self.report_summary}',
            'channel': self.channel,
            'attachments': [],
        }

        results_attachment = {
            'text': 'All tests are passing successfully! :sparkles:',
            'color': 'good',
        }

        if self.failed_tests_count > 0:
            results_attachment.update({
                'text': ('Failed Tests:\n'
                         '```{}```'.format('\n'.join(self.failed_test_names))),
                'color': 'bad',
            })

        if self.results_url:
            results_attachment.update({
                'actions': [
                    {
                        'type': 'button',
                        'text': 'View detailed test report',
                        'url': self.results_url,
                        'style': 'primary'
                    }
                ]
            })

        message['attachments'].append(results_attachment)

        return message

    def send_message(self) -> requests.Response:
        return requests.post(
            url=self.webhook_url,
            json=self.create_message(),
        )

    def pytest_runtest_logreport(self, report) -> None:
        # pytest will otherwise double-count tests if they fail in setup or teardown
        if (report.when in {'setup',
                            'teardown'} and not report.passed) or report.when == 'call' and report.outcome != 'rerun':
            self.reports[Outcome(report.outcome)].append(report)

    def pytest_terminal_summary(self, terminalreporter) -> None:
        if hasattr(terminalreporter.config, 'workerinput'):
            return
        terminalreporter.write_sep('-', 'Results Sent to Slack')

    def pytest_sessionstart(self, session) -> None:
        self.session_start = time.time()

    def pytest_sessionfinish(self, session, exitstatus) -> None:
        self.session_end = time.time()
        if self.failure_only is None or self.failure_only.lower() == 'false':
            self.send_message()
            print('All Test results sent to Slack')
        elif self.failure_only.lower() == 'true' and self.failed_tests_count > 0 and exitstatus == 1:
            self.send_message()
            print('Test results with failures sent to Slack')
        else:
            print(f"No Slack alert sent")


def pytest_addoption(parser: Parser):
    group = parser.getgroup('slack')
    group.addoption(
        '--slack-webhook-url',
        help='Slack webhook URL to send test results',
        default=os.getenv('SLACK_WEBHOOK_URL'),
    )
    group.addoption(
        '--slack-channel',
        help='Slack channel to send test results',
        default=os.getenv('SLACK_CHANNEL'),
    )
    group.addoption(
        '--slack-results-url',
        help='URL to results page for link in Slack message',
        default=os.getenv('SLACK_RESULTS_URL'),
    )
    group.addoption(
        '--slack-failure-only',
        help='Alert only on test failures',
        default=os.getenv('SLACK_FAILURE_ONLY'),
    )


def pytest_configure(config: Config):
    slack_webhook_url = config.option.slack_webhook_url
    if slack_webhook_url and not hasattr(config, 'workerinput'):
        plugin = SlackPlugin(
            webhook_url=slack_webhook_url,
            channel=config.option.slack_channel,
            results_url=config.option.slack_results_url,
            failure_only=config.option.slack_failure_only,
        )
        config._slack = plugin
        config.pluginmanager.register(plugin)


def pytest_unconfigure(config: Config):
    plugin = getattr(config, '_slack', None)
    if plugin:
        del config._slack
        config.pluginmanager.unregister(plugin)
