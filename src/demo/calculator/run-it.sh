#!/usr/bin/env bash


pushd ../ &> /dev/null || exit 1
CUR_DIR="$(pwd)"
export PYTHONPATH="${CUR_DIR}"
python3 calculator/main.py
popd &> /dev/null || exit 1
