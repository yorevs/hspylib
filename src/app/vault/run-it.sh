#!/usr/bin/env bash

[[ -f .env ]] && source .env
pushd ../ &> /dev/null || exit 1
CUR_DIR="$(pwd)"
export PYTHONPATH="${CUR_DIR}"
python3 vault/main.py "$@"
popd &> /dev/null || exit 1
