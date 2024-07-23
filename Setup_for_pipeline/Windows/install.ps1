$SCRIPT_DIR=$PSScriptRoot
 
$PYTHON_EXE="python"
 
$PYTHON_VERSION = & "$PYTHON_EXE" "--version"
 
$MAJOR = select-string -pattern "3.9" -InputObject $PYTHON_VERSION
 
if (! $MAJOR){
    $PYTHON_EXE="python3"
    $PYTHON_VERSION = & "$PYTHON_EXE" "--version"
    $MAJOR = select-string -pattern "3.9" -InputObject $PYTHON_VERSION
 
    if (! $MAJOR){
        echo "Error: Using python version $PYTHON_VERSION. Please use Python 3.9"
        exit 1
    }
 
}
 
push-location -Path "$SCRIPT_DIR/.."
invoke-expression -Command "$PYTHON_EXE -m venv ./venv"
 
. "./venv/Scripts/activate.ps1"
$WHEEL= Get-ChildItem -Name |  select-string -Pattern whl
pip install "$WHEEL"
pop-location