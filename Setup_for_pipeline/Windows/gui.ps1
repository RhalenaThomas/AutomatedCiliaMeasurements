$SCRIPT_DIR=$PSScriptRoot
 
if (! (Test-Path env:VIRTUAL_ENV) -and ! (Test-Path -Path "$SCRIPT_DIR/../venv")) {
    powershell -noexit -executionpolicy bypass -File install.ps1
}
 
if  (! (Test-Path env:VIRTUAL_ENV)){
    . "$SCRIPT_DIR/../venv/Scripts/activate.ps1"
}
 
# Open the GUI
automated_cilia_measurements_gui