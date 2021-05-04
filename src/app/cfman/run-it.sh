#!/usr/bin/env bash

[[ -f .env ]] && source .env
pushd ../ &>/dev/null || exit 1
CUR_DIR="$(pwd)"
export PYTHONPATH="${CUR_DIR}"
popd &>/dev/null || exit 1
python3 src/main/__main__.py "$@"
popd &>/dev/null || exit 1
