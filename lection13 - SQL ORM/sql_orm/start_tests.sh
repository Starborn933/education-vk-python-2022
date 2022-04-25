#!/bin/bash

cd code || exit 1

pytest -s -l -v tests/test_mysql.py --alluredir /tmp/alluredir -n "${THREADS:-0}"