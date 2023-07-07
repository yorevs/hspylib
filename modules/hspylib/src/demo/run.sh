#!/usr/bin/env bash

export PYTHONPATH="../../"

demos="$(find $PYTHONPATH -type f -iname '*_demo.py')"

if [[ $# -eq 0 ]]; then
  echo "Please select one demo to run:"
  echo ''
  echo "${demos//${PYTHONPATH}\/src\/demo\//}"
  echo ''
else
  python3 "${@}"
fi
