# Make relations datafram module

This module is required in the `AutomatedCiliaMeasurements` pipeline.

## Usage

## Description

## Arguments

## Helper functions

* `split_centriole_col(c2c_pairings)`

    Splits pair of centrioles mathced with nucleus from [center to center](center2center.md) processing into two columns.

    ### Parameters

    * `c2c_pairings`

        Dataframe of all pairings betwen nuclei, cilia, and centrioles, read from output of [center to center module](center2center.md) (`c2c_output.csv`).

    ### Returns

    Dataframe of all pairings betwen nuclei, cilia, and centrioles each split into their repective columns.

* `normalize_and_clean(measurements_nuc, measurements_cilia, measurements_cent, c2c_pairings)`

    Merge dataframes CellProfiler and [center to center](center2center.md) dataframes, adding binary and distance columns.

    ### Parameters

    * `measurements_nuc` 
    
        Dataframe of nuclei measurements, usually read from CellProfiler csv file.
    
    * `measurements_cilia` 
    
        Dataframe of cilia measurements, usually read from CellProfiler csv file.
    
    * `measurements_cent` 
    
        Dataframe of centriole measurements, usually read from CellProfiler csv file.
    
    * `c2c_pairings` 
    
        Dataframe of all pairings betwen nuclei, cilia, and centrioles each split into their repective columns.

    ### Returns

    Merged dataframe with specific selected and renamed columns from the above dataframe. Refer to [implementation details](#implementation-details) for more information.

## Implementation details