# AutomatedCiliaMeasurements
A Pipeline to identify and measure features of cilia, nuclei, and centrioles from microscopy images and to match cilia with nuclei and centrioles using CellProfiler and Python.  The python pipeline is easy to install and runs by one command inside a virtual enviroment that automatically installs all the needed packages. 

# Installation

1) Copy this github repository to download all the needed files. You can do this by clicking on the green button that says "Code".  Choose your download method: select "Download ZIP" if you do not use github.
2) Unzip you folder
3) Open the file "Running_Instructions" detailed instructions.
4) You will have all the files to run the python pipeline with our data as a test. 

# Pipeline Usage

A) CellProfiler: Install and run a Cellprofiler pipeline using our cell profiler projects as a template. See this site for how to use Cellprofiler.  https://cellprofiler.org/getting-started
   Run your CellProfiler analysis. The outputs must all be in one folder and are required for python pipeline to function. Be sure to keep the default prefix provided by CellProfiler.  The Python pipeline will look for specific file names. 
B) Python automated cilia detection: Install python pipeline from this github repository (see above). Initiate the virtual enviroment. Run the command code.


# Pipeline compenents and script details: 
A) Cellprofiler. 
(1) We have provided cell profiler pipelines but these must be adapted for each use case via the cell profiler GUI. Be certain to keep all the same outputs selected. 
(2) The outputs from cell profiler are the input speadsheets for the python scripts. 

B) Python pipeline to match cilia and centroiles with nuclei, summarize feature measurements and generate summary plots. The following scripts are part of the pipeline.

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



