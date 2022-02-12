#!/usr/bin/env bash

[[ -f .env ]] && source .env
CURDIR=$(pwd)
export PYTHONPATH="${CURDIR}/src/main"
python3 src/main/versioner/__main__.py "$@"
