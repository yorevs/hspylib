#!/usr/bin/env bash

[[ -f .env ]] && source .env
CURDIR=$(pwd)
export PYTHONPATH="${CURDIR}/src/main"
python3 src/main/%APP_NAME%/__main__.py "$@" &
