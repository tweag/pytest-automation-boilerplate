#!/bin/sh

# Run API tests
python -m pytest -v -s --gherkin-terminal-reporter  --html="./output/reports/" --tags=$1 --self-contained-html --reruns 1 --reruns-delay 2 --alluredir=allure-results