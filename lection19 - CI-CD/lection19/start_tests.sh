#!/bin/bash

cd code

pytest -s -l -v "${TESTS_PATH}" -n "${THREADS:-2}" --alluredir /tmp/allure
