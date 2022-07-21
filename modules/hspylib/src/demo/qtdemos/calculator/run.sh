#!/usr/bin/env bash

pushd ../ &>/dev/null || exit 1
CUR_DIR="$(pwd)"
export PYTHONPATH="${CUR_DIR}:${PYTHONPATH}"
python3 calculator/__main__.py
popd &>/dev/null || exit 1
