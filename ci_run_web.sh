#!/bin/sh

# Run Web tests
python -m pytest -vv -s  --gherkin-terminal-reporter --driver=Remote --selenium-host "$1":"$2""@hub-cloud.browserstack.com" --variables=$3 --html="./output/reports/"  \
--tags="$4" --reruns 1 --reruns-delay 2 --self-contained-html --capability headless False --base-url=$5 --slack-webhook-url=$6 --slack-channel=pytest-test-automation \
--slack-results-url=https://tweag.github.io/pytest-automation-boilerplate --teams-webhook-url=$7 \
--teams-results-url=https://tweag.github.io/pytest-automation-boilerplate --slack-failure-only=true --teams-failure-only=true