#!/bin/bash

# Get the full directory of the running script
SCRIPT_DIR="$( cd -- "$(dirname "$0")" > /dev/null 2>&1 ; pwd -P )"

# Get the root directory of the repo
ROOT_DIR="$(cd -- "$SCRIPT_DIR/../.."; pwd -P )"

# Check if python3.9 is installed
PYTHON_EXE="python"
PYTHON_VERSION=$("$PYTHON_EXE" --version 2>&1)
$(echo "$PYTHON_VERSION" | grep -q "3.9")
if [ "$?" -ne 0 ]; then
    PYTHON_EXE="python3"
    PYTHON_VERSION=$("$PYTHON_EXE" --version 2>&1)
    $(echo "$PYTHON_VERSION" | grep -q "3.9")
    if [ "$?" -ne 0 ]; then
        PYTHON_EXE="python3.9"
        PYTHON_VERSION=$("$PYTHON_EXE" --version 2>&1)
        $(echo "$PYTHON_VERSION" | grep -q "3.9")
        if [ "$?" -ne 0 ]; then
            echo "Error: Using python version $PYTHON_VERSION. Please use Python 3.9"
            exit 1
        fi
    fi
fi

# Change directory to root dir
cd "$ROOT_DIR"

# Create and activate virtual env
$("$PYTHON_EXE" -m venv ./venv)
. "./venv/bin/activate"

# Get .whl file and install project
WHEEL=$(find . -name "*.whl")
pip install "$WHEEL"

# # Open the GUI
# automated_cilia_measurements_gui