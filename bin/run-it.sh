#!/usr/bin/env bash

CUR_DIR="$(pwd)"

export PYTHONPATH="${CUR_DIR}/src/main"

pushd "${CUR_DIR}/src/main" &> /dev/null || exit 1
python3 main.py
popd &> /dev/null || exit 1

exit 0
