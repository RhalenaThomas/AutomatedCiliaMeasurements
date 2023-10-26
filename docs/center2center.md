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

A folder `center2center_output` is created at the `-output` path specified as an argument.

The fields `ImageNumber`, `Location_Center_X` and `Location_Center_Y` are read from the CellProfiler CSV files (from `-input` argument specified) into respective dataframes.
The dataframes (representing nuclei, cilias and centrioles) are then grouped by their `ImageNumber`.

For each `ImageNumber`:

* The cells, centrioles and cilia associated with that `ImageNumber` are each made into a separate list.

* Each centriole is matched to its closest nucleus.

    * Each nucleus can have a maximum of 2 centrioles.

    * A threshold of distance is also set.

    * If, for any matching, the distance is beyond threshold, the centriole is invalidated.

    * If, for any nucleus, more than 2 centrioles are matched the furthest one(s) is invalidated.

    * Any invalidated centriole is added to a list of indices which is removed from initial list of centrioles built per `ImageNumber`.

* The same process is repeated for each cilium matched to its closest nucleus, with a maximum of 1 cilium matched with any particular nucleus.

* The matched centrioles and cilias are combined with their associated nucleus, displaying the following fields: `ImageNumber`, `Nucleus`, `PathLengthCentriole`, `Centriole`, `PathLengthCilia` and `Cilia`.

