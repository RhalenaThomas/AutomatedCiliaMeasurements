# Installing and Running the Program

Note that Python 3.9 is required. The application does not work for other versions.

## Linux/Mac

First, navigate to the Linux_and_Mac folder. To use the CLI,  run `sh install.sh`, `source ../venv/bin/activate` and finally `automated_cilia_measurements --help`.

Currently the GUI is not complete. Previously, to run the GUI, you would run `sh gui.sh`. 

# code to run Command line 
For MacOS or Linux

```
# navigate to the Linux_and_Mac folder

cd /release/Linux_and_Mac

# run 
sh install.sh

# navigate back to the parent directory
cd ../..    # you need to be in the home github repo folder to run the pipeline
source venv/bin/activate

```


Windows

First, navigate to the Windows folder in the File Explorer.  To run the GUI, right click on `gui.ps1` and select `Run in Powershell`.  To use the CLI, right click on `install.ps1` and select `Run in Powershell`.  Then, in a Powershell terminal (while running as administrator and making sure you have the correct permissions to run commands), type `. "../venv/Scripts/activate.ps1"` 



# Running command line in virtual enviroment

 
Once you have activated the virtual enviroment and navigated to the correct folder run the command to run the python pipeline

`python acm/script.py -i <CellProfiler_csvs_path> -o <Desired output path> --scale <pixle to micron converstion factor>` 


```
# code to run
# example code 

python acm/script.py -i /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/Neurons_cp_outs_csvs/ -o /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/Neurons/ --scale 3.52



```


automated_cilia_measurements --help # Ignore this for now. There are multiple versions mismatched right now

# Errors - missing pandas

pip install pandas
pip install matplotlib
pip install skikit-learn

