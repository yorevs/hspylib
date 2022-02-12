#!/usr/bin/env bash

[[ -f .env ]] && source .env
CURDIR=$(pwd)
export PYTHONPATH="${CURDIR}/src/main"
python3 src/main/kafman/__main__.py "$@" &
