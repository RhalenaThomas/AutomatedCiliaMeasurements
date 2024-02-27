# Installing and Running the Program

Note that Python 3.9 is required. The application does not work for other versions.

## Linux/Mac

First, navigate to the Linux_and_Mac folder. To use the CLI,  run `sh install.sh`, `source ../venv/bin/activate` and finally `automated_cilia_measurements --help`.

Currently the GUI is not complete. Previously, to run the GUI, you would run `sh gui.sh`. 

# code to run directly in terminal
cd /release/Linux_and_Mac
sh install.sh
cd ../..
source venv/bin/activate
`python acm/script.py -i <CellProfiler_csvs_path> -o <Desired output path>` # example code

# pathway to cell profile output /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/sample_csvs
# pathway to output /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/test_out2
# code to run
python acm/script.py -i /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/Neuron_cellprofiler_output_csvs -o /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs


automated_cilia_measurements --help # Ignore this for now. There are multiple versions mismatch now



## Windows

First, navigate to the Windows folder in the File Explorer.  To run the GUI, right click on `gui.ps1` and select `Run in Powershell`.  To use the CLI, right click on `install.ps1` and select `Run in Powershell`.  Then, in a Powershell terminal (while running as administrator and making sure you have the correct permissions to run commands), type `. "../venv/Scripts/activate.ps1"` and run `automated_cilia_measurements --help`.

