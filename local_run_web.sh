#!/bin/sh

# Run API tests
python -m pytest -v -s  --gherkin-terminal-reporter --driver=Chrome  --html="./output/reports/" --self-contained-html  --capability headless True  --reruns 1 --reruns-delay 2 --tags="web_tests" -n 2