#!/bin/sh

# Run API tests
python -m pytest -vv -s --html="./output/reports/" --tags="$1" --self-contained-html --reruns 1 --reruns-delay 2 --alluredir=allure-results \
--slack-webhook-url=$2 --slack-channel=pytest-test-automation --slack-results-url=https://tweag.github.io/pytest-automation-boilerplate --teams-webhook-url=$3 \
--teams-results-url=https://tweag.github.io/pytest-automation-boilerplate --slack-failure-only=true --teams-failure-only=true -n=4