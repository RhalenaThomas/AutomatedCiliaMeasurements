# AutomatedCiliaMeasurements
A Pipeline to identify and measure features of cilia, nuclei, and centrioles from microscopy images and to match cilia with nuclei and centrioles using CellProfiler and Python.  There is an option of Graphical User Interface (GUI) and command line interface (CLI) for easy use for different user types. 

# Pipeline compenents: 
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

How to Use:
(1) Download release 

(2) Follow release README instructions

