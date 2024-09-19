#!/bin/sh

# path to project folder, this_file/../
ROOT_FOLDER=$(
    cd "$(dirname "$0")/.." || exit
    pwd
)
cd "$ROOT_FOLDER" || exit

# shellcheck source="../.venv/bin/activate"
. "./.venv/bin/activate"

# run scalene
# TODO: add concurrent/sequential flag
scalene main.py transcriptor
