# <MODULE_NAME>

## Description

## Arguments

## Helper functions

* `setup_for_clustering(c2c_pairings, tuned_parameters)`

    Set up clustering visualization and split centrioles into two columns.

    ### Parameters

    * `c2c_pairings`
    
        Dataframe of all pairings betwen nuclei, cilia, and centrioles read from output of [center to center module](center2center.md) (`c2c_output.csv`).
    
    * `tuned_parameters` 
    
        Parameters for KMeans

    ### Returns

    * scores 
    * clf 
    * pca_2d 
    * pca_7d 
    * c2c_pairings

## Implementation details