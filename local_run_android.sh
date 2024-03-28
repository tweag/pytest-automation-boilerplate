#!/bin/sh

# Run API tests
python -m pytest -vv -s  --disable-warnings --gherkin-terminal-reporter --driver=Appium  --html="./output/reports/" --self-contained-html  \
--variables="env_configs/android_mobile_docker.json"  --reruns 1 --reruns-delay 2 --tags="android_mobile_tests"