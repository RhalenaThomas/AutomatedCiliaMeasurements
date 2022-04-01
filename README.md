# AutomatedCiliaMeasurements
Pipeline to measure cilia, nuclei, and centrioles, and to measure which cilia are close to which nuclei and centrioles using CellProfiler and Python.

# How to Use
Step 1: Download the repository from https://github.com/xosneha/AutomatedCiliaMeasurements

Step 2: Run the CellProfiler pipeline, and make sure that you ensure (1) all the CSVs end up in one folder and (2) all the images end up in a different folder. This can be edited by changing the output folder of the CellProfiler pipeline.

Step 3: Run the runner.py program.  This will prompt you to select a folder where you want your results to go, then to select where the results of step (2) went, and eventually, will ask you which parts of the pipeline you want to run.  

Pipeline parts: 
(1) center2center.py: Algorithm that matches nuclei with cilia and centrioles, and determines which cilia and centrioles are valid (being paired with a nucleus means they are valid, and being unpaired means they are noise).

(2) clustering.py: X-Means clustering on valid cilia results from output.

(3) label_cprof_im.py: Labels CellProfiler images with numbers from CellProfiler spreadsheets.  DOES NOT take the center2center algorithm into account (i.e. this will not differentiate between invalid/valid measurements).

(4) data_table.py: Makes a data table with a couple of key summary measurements: average number of cilia, average number of nuclei, present cilia/present nuclei, average nuclei area, average cilia length, average cilia area for all images.

(5) label_c2c.py: Labels the results of the c2c pipeline, with the cilia, centriole, and nuclei being displayed on one image that is a combined image of the three.  

(6) label_valid_cilia.py: Labels valid instances of one organelle (e.g. all valid cilia onto images of just cilia). This can be the nuclei (channel 01), cilia (channel 02), or centriole (channel 03). 

(7) accuracy_checker: Checks accuracy of cilia counts given a CSV that shows the number of false positives and false negatives in the results. 
