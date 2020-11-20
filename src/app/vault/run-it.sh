#!/usr/bin/env bash

export HHS_VAULT_USER=
export HHS_VAULT_FILE=
export HHS_VAULT_PASSPHRASE=MTIzNDU=

pushd ../ &> /dev/null || exit 1
CUR_DIR="$(pwd)"
export PYTHONPATH="${CUR_DIR}"
python3 vault/main.py "$@"
popd &> /dev/null || exit 1
