#!/bin/sh

# Run Web tests
python -m pytest -v -s  --gherkin-terminal-reporter --driver=Remote --selenium-host "$1":"$2""@hub-cloud.browserstack.com" --variables=$3 --html="./output/reports/"  \
--tags=$4 --reruns 1 --reruns-delay 2 --self-contained-html --capability headless False --slack-webhook-url=$5 --slack-channel=pytest-test-automation  \
--slack-results-url=https://tweag.github.io/pytest-automation-boilerplate --teams-webhook-url=$6  \
--teams-results-url=https://tweag.github.io/pytest-automation-boilerplate --base-url=$7