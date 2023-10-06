# Center to center module

This module is required in the `AutomatedCiliaMeasurements` pipeline.

## Description 

From CellProfiler CSV files (Nucleus, Centriole, and Cilia), match valid centrioles and cilia to cell.

## Usage

`center2center.py [-h] -i <INPUT_PATH> -o <OUTPUT_PATH>`

## Arguments

* `-h` or `help` (Optional)

    Flag to print module usage.

* `-i` or `-input` (Required)

    Path of directory containing:

    * <CellProfiler_Nucleus_csv_file>

    * <CellProfiler_Cilia_csv_file>

    * <CellProfiler_Centriole_csv_file>

* `-o` or `-output` (Required)

    Path of directory where output files of the module is created.

    Output files are:

    * `c2c_output.csv`
    
        Nucleus with their matched centrioles and cilia and their respective path length.
        The fields are:
        * ImageNumber
        * Nucleus
        * PathLengthCentriole
        * Centriole
        * PathLengthCilia
        * Cilia

    * `new_cent.csv`

    * `new_cilia.csv`

## Helper functions

## Implementation details
