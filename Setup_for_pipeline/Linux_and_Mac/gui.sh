SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Check if install.sh was ran. If it wasn't, then run it.
if [[ $VIRTUAL_ENV = '' ]] && [[ ! -d "$SCRIPT_DIR/../venv" ]]; then
    sh install.sh
fi

# Source virtual env
if [[ $VIRTUAL_ENV = '' ]]; then
    source "$SCRIPT_DIR/../venv/bin/activate"
fi

# Open the GUI
automated_cilia_measurements_gui