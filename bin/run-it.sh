#!/usr/bin/env bash

CUR_DIR="$(pwd)"

export PYTHONPATH="${CUR_DIR}/src/main"

pushd "${CUR_DIR}/src/main" &> /dev/null || exit 1
pyrcc5 resources.qrc -o resources_rc.py
python3 main.py
popd &> /dev/null || exit 1

exit 0
