# Get Script directory
$SCRIPT_DIR=$PSScriptRoot

# Move to repo root
Set-Location "$SCRIPT_DIR/../.."

# Check python version
$PYTHON_EXE="python"
$PYTHON_VERSION=& "$PYTHON_EXE" "--version"
$MAJOR=select-string -pattern "3.9" -InputObject $PYTHON_VERSION
 
if (! $MAJOR){

    $PYTHON_EXE="python3"
    $PYTHON_VERSION=& "$PYTHON_EXE" "--version"
    $MAJOR=select-string -pattern "3.9" -InputObject $PYTHON_VERSION
 
    if (! $MAJOR){

        $PYTHON_EXE="python3.9"
        $PYTHON_VERSION=& "$PYTHON_EXE" "--version"
        $MAJOR=select-string -pattern "3.9" -InputObject $PYTHON_VERSION

        if (! $MAJOR){
            Write-Output "Error: Using python version $PYTHON_VERSION. Please use Python 3.9"
            exit 1
        }
    }
 
}

# Create and activate virtual environment
invoke-expression -Command "$PYTHON_EXE -m venv ./venv"
. "./venv/Scripts/activate.ps1"

# Install dependencies and project
$WHEEL=Get-ChildItem -Path .\ -Filter *.whl -Recurse | ForEach-Object { $_.FullName }
pip install "$WHEEL"

# Launch GUI
automated_cilia_measurements_gui
