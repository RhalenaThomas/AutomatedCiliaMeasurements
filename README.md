# AutomatedCiliaMeasurements
A Pipeline to identify and measure features of cilia, nuclei, and centrioles from microscopy images and to match cilia with nuclei and centrioles using CellProfiler and Python. The python pipeline is easy to install and runs by one command inside a virtual enviroment that automatically installs all the needed packages. Cell profiler is used to detect nuclei, cilia and centrioles and take measurement of each object. The python pipeline matches cilia and centrioles to nuclei selecting true cilia. 

# Installation

1) Copy this github repository to download all the needed files. You can do this by clicking on the green button that says "Code".  Choose your download method: select "Download ZIP" if you do not use github.
2) Unzip the folder. You will have all the files to run the python pipeline with our data as a test. 


# Pipeline Usage

Part 1 CellProfiler 
* Install and run a Cellprofiler pipeline using our cell profiler projects as a template. See this site for how to use Cellprofiler.  https://cellprofiler.org/getting-started. You will need to change the file location of your input files and your file extensions to match the channels appropriately in Cell Profiler. You will also need to optimize your settings for detecting objects in Cell Profiler. 
   
1. Open one of the provided Cell profiler projects eg "cilia_pipeline_Neurons.cpproj" 
2. Select "Images" from the Cell profiler menu on the left. Highlight all images, right click and select to clear all images. 
3. Drag your images to analyze into the window.
4. You must have images from 3 channels.  In the left menu select "NamesAndTypes". Change the file criteria for nuclei, cilia and centroile staining to match your file names.
5. At this point you can test the settings in Cell Profiler by unclicking all the eye icons and selecting "Start Test Mode" in the bottom left of the window. Click "play" for each step and look at the outputs. Click on each "IdentifyPrimaryObjects" and change the settings until you are satisfied with the areas selected (and outlined) by Cell profiler. Note, cell profiler converts to pixels, the size settings in our images will necessarily match other images. Additionally the amount of background and signal saturation will change the detection as well. Setting must be optimized for each dataset. 
6. Before running the Cell Profiler analysis on all images, click the eye icons to cross them out and turn them grey (this will speed up running time)
7. In the menu on the left, select "ExportToSpreadsheet" ** Do not change the filename prefix **. Change the output file location to the folder you want all the output to go into.
8. Click "Analyze Images" in the bottom left of the window to run the analysis.
9. In your file finder, go to the output folder and check that the csv files are present and all files are in this format MyExpt_*name*.csv. The output folder should contain MyExpt_Centriole.csv, MyExpt_Cilia.csv, MyExpt_Nucleus.csv, MyExpt_Experiment.csv, MyExpt_Image.csv. These files are the required input for the python pipeline and must have these names. 

Part 2 Python Pipeline
* The python pipeline requires Python 3.9, you must have Python 3.9 installed. To run the python pipeline you will install a virtual environment and then activate this environment in the future. To make running the pipeline easier you can use VSCode https://code.visualstudio.com/download. Using VS code you can write your commands in a text file and copy paste into the terminal/powershell. 

1. In VScode open a new terminal (this will be powershell if you are using windows)
2. Set up your virtual environment (venv) and activate.

For Windows : 

Navigate to the folder "Setup_for_pipeline" 
```
# you must use your actual file pathway
# If your file pathway name contains spaces you can put the whole text in quotes

cd AutomatedCiliaMeasurements\Setup_for_pipeline\
# or 
cd "My Folder\AutomatedCiliaMeasurements\Setup_for_pipeline\"
```
Now run a file to install the packages needed for running the python pipeline
```
.\install.ps1

```
Now you will activate the enviroment. This step must be done each time you wish to run the pipeline
```
. "../venv/Scripts/activate.ps1"
```

After running this command you should now have (venv) beside your terminal prompt. This means you are now in the virtual environment.

3. Return to the parent folder (the main "AutomatedCiliaMeasurements") folder.
```
cd ..\..   # windows
cd ../..   # mac/linux
```
4. Run the pipeline. 
You will need to know the file pathway of your Cell Profiler output folder and the new folder (make one) where you want the Python Pipeline outputs to go. 
```
# general command
`python acm/script.py -i <CellProfiler_csvs_path> -o <Desired output path> --scale <pixle to micron conversion factor>` 

# python acm/script.py is the python script to call the pipeline
# -i is the input directory (the CellProfiler output folder)
# -0 is the output directory (the new output folder)
# --scale is teh pixle to micron conversion factor and is a numerical value - you must calculate this value from your images

# example useage

python acm/script.py -i /GITHUB/AutomatedCiliaMeasurements/Neurons_cp_outs_csvs/ -o /GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/Neurons/ --scale 0.2841
```




# Pipeline compenents and script details: 
A) Cellprofiler. 
(1) We have provided cell profiler pipelines but these must be adapted for each use case via the cell profiler GUI. Be certain to keep all the same outputs selected. 
(2) The outputs from cell profiler are the input speadsheets for the python scripts. 

B) Python pipeline to match cilia and centroiles with nuclei, summarize feature measurements and generate summary plots. The following scripts are part of the pipeline. Note that the python script with arguments to run the pipeline is in the folder "amc". 

(1) center2center: Algorithm that matches nuclei with cilia and centrioles, and determines which cilia and centrioles are valid (being paired with a nucleus means they are valid, and being unpaired means they are noise).

(2) clustering: X-Means clustering on valid cilia results from output.

(3) label_cprof_im: Labels CellProfiler images with numbers from CellProfiler spreadsheets.  DOES NOT take the center2center algorithm into account (i.e. this will not differentiate between invalid/valid measurements).

(4) data_table: Makes a data table with a couple of key summary measurements: average number of cilia, average number of nuclei, present cilia/present nuclei, average nuclei area, average cilia length, average cilia area for all images.

(5) label_c2c: Labels the results of the c2c pipeline, with the cilia, centriole, and nuclei being displayed on one image that is a combined image of the three.  

(6) label_valid_cilia: Labels valid instances of one organelle (e.g. all valid cilia onto images of just cilia). This can be the nuclei (channel 01), cilia (channel 02), or centriole (channel 03). 

(7) accuracy_checker: Checks accuracy of cilia counts given a CSV that shows the number of false positives and false negatives in the results. 

(8) pixels_to_measurement: Converts pixels to measurements like micrometers if given a conversion factor 

(9) summary_measurements: Makes scatterplots, histograms, and bar plots by image for a variety of factors

Standalone scripts:
(1) standalone_bokeh: Makes Bokeh server showing summary measurements 

(2) standalone_clustering_test: For use in testing different methods and parameters of clustering 

(3) standalone_cprof_label: Labels CellProfiler images 



