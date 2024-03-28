#!/bin/sh

# Run Web tests
python -m pytest -vv -s  --gherkin-terminal-reporter --driver=Remote --selenium-host "$1":"$2""@hub-cloud.browserstack.com" --variables=$3 --html="./output/reports/"  \
--tags=$4 --reruns 1 --reruns-delay 2 --self-contained-html --capability headless False --base-url=$5