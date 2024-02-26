import pandas as pd
import numpy as np
from pathlib import Path
import math
import argparse
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from helper import match, read_cellprofiler_csv

def main(**args):

    args = args or parse_args()

    # Paths handling
    cellprofiler_input_path = Path(args["input"])
    output_path = Path(args["output"], "output")
    output_path.mkdir(parents=True, exist_ok=True)
    data_tables_path = Path(output_path, "data_tables")
    data_tables_path.mkdir(parents=True, exist_ok=True)
    plots_path = Path(output_path, "plots")
    plots_path.mkdir(parents=True, exist_ok=True)

    # Read CellProfiler CSVs into dataframes
    nucleus_df = read_cellprofiler_csv(Path(cellprofiler_input_path, "MyExpt_Nucleus.csv"), "Nucleus")
    centriole_df = read_cellprofiler_csv(Path(cellprofiler_input_path, "MyExpt_Centriole.csv"), "Centriole")
    cilia_df = read_cellprofiler_csv(Path(cellprofiler_input_path, "MyExpt_Cilia.csv"), "Cilia")

    # Convert Pixels to microms
    if args["scale"]:
        nucleus_df, cilia_df, centriole_df = convert_to_microm(float(args["scale"]), nucleus_df, cilia_df, centriole_df)

    # Build c2c dataframe
    c2c_df = c2c(nucleus_df, centriole_df, cilia_df)
    c2c_df.to_csv(Path(data_tables_path, "c2c.csv"), index=False)

    # Append all organelles features
    all_measures_by_cilia_df = append_features(c2c_df, nucleus_df, centriole_df, cilia_df)
    all_measures_by_cilia_df.to_csv(Path(data_tables_path, "all_measures_by_cilia.csv"), index=False)

    # Calculate the mean of each feature for all matched organelles of each image
    organelle_id_fields = ["Nucleus", "Centriole1", "Centriole2", "Cilia"]
    mean_per_image_df = all_measures_by_cilia_df.drop(organelle_id_fields, axis=1).groupby("ImageNumber").mean().add_prefix("Mean_")
    mean_per_image_df.reset_index(inplace=True)
    mean_per_image_df.to_csv(Path(data_tables_path, "mean_per_image.csv"), index=False)

    summary_counts_df = summary_count(c2c_df, nucleus_df, centriole_df, cilia_df)
    summary_counts_df.to_csv(Path(data_tables_path, "summary_counts.csv"), index=False)
    
    plot_mean_per_image(mean_per_image_df, plots_path)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", help="path to directory with CellProfiler CSVs", required=True
    )

    parser.add_argument(
        "-o", "--output", help="output folder path", required=True
    )

    parser.add_argument(
        "-x", "--scale", help="Multiplication factor for pixel to microms", required=False
    )
    
    return vars(parser.parse_args())

def convert_to_microm(
    multiply_factor, measurements_nuc, measurements_cilia, measurements_cent
):
    """
    Convert measurements to micrometers
    :param multiply_factor: Conversion factor
    :param measurements_nuc: Nuclei measurements to convert
    :param measurements_cilia: Cilia measurements to convert
    :param measurements_cent: Centriole measurements to convert
    :returns: Measurements with conversion factor updated
    """

    to_multiply_x = [
        "AreaShape_EquivalentDiameter",
        "AreaShape_MajorAxisLength",
        "AreaShape_MaxFeretDiameter",
        "AreaShape_MaximumRadius",
        "AreaShape_MeanRadius",
        "AreaShape_MedianRadius",
        "AreaShape_MinFeretDiameter",
        "AreaShape_MinorAxisLength",
        "AreaShape_Perimeter",
    ]

    to_multiply_2x = ["AreaShape_Area", "AreaShape_BoundingBoxArea"]

    for col in to_multiply_x:
        measurements_nuc[col] = multiply_factor * measurements_nuc[col]
        measurements_cilia[col] = multiply_factor * measurements_cilia[col]
        measurements_cent[col] = multiply_factor * measurements_cent[col]

    multiply_factor_2x = multiply_factor * multiply_factor

    for col in to_multiply_2x:
        measurements_nuc[col] = multiply_factor_2x * measurements_nuc[col]
        measurements_cilia[col] = multiply_factor_2x * measurements_cilia[col]
        measurements_cent[col] = multiply_factor_2x * measurements_cent[col]

    return measurements_nuc, measurements_cilia, measurements_cent

def c2c(nucleus_df, centriole_df, cilia_df):
    # Initialize c2c_df
    c2c_df = pd.DataFrame(columns=['ImageNumber', 'Nucleus', 'Centriole1', 'Centriole2', 'Cilia', 'Nuc_Cent1', 'Nuc_Cent2', 'Nuc_Cil'])

    # Create location coordinates dictionary from dataframes, required for cilia and centriole only(for easy distance calculation)
    centriole_loc_dict = centriole_df.groupby("ImageNumber")[["Centriole", "Location_Center_X", "Location_Center_Y"]].apply(lambda x : x.set_index("Centriole").to_dict(orient="index")).to_dict()
    cilia_loc_dict = cilia_df.groupby("ImageNumber")[["Cilia", "Location_Center_X", "Location_Center_Y"]].apply(lambda x : x.set_index("Cilia").to_dict(orient="index")).to_dict()
    
    # Group dataframe using ImageNumber
    grouped_nucleus = nucleus_df.groupby("ImageNumber")
    grouped_centriole = centriole_df.groupby("ImageNumber")
    grouped_cilia = cilia_df.groupby("ImageNumber")

    # Iterate over groups 
    # Note: groups in grouped_nucleus, grouped_centriole and grouped_cilia are expected to be aligned
    for key in grouped_nucleus.groups.keys():

        # Fetch respective group
        nucleus_group = grouped_nucleus.get_group(key)
        centriole_group = grouped_centriole.get_group(key)
        cilia_group = grouped_cilia.get_group(key)

        coord_fields = ["Location_Center_X", "Location_Center_Y"]
        centriole_feature_threshold_field = "AreaShape_MeanRadius"

        #region : Nucleus - Centriole Matching

        # Match nucleus (parent) with closest 2 centrioles (child) 
        nucleus_centriole_match_dict = match(
            parents=nucleus_group.loc[:, coord_fields].values, 
            childs=centriole_group.loc[:, coord_fields].values, 
            arity=2,
            thresholds=nucleus_group[centriole_feature_threshold_field].to_list()
        )

        # Make df from dict and rename columns
        nucleus_centriole_match_df = pd.DataFrame.from_dict(nucleus_centriole_match_dict, orient='index')
        nucleus_centriole_match_df.rename(columns={"path_length":"Nuc_Cent", "parent":"Nucleus"}, inplace=True)
        nucleus_centriole_match_df.reset_index(inplace=True, names="Centriole") 

        # Drop unmatched/invalid centriole
        nucleus_centriole_match_df.drop(nucleus_centriole_match_df[nucleus_centriole_match_df.Nucleus == -1].index, inplace=True)   
        
        # Increment Centriole and Nucleus number since they are 1-based
        nucleus_centriole_match_df["Centriole"] += 1
        nucleus_centriole_match_df["Nucleus"] += 1

        # Sort values by nucleus number and distance from nucleus
        nucleus_centriole_match_df = nucleus_centriole_match_df.sort_values(by=['Nucleus', 'Nuc_Cent']).groupby(['Nucleus'], as_index=False).agg(list)

        # Split Centriole number and distances from nucleus
        try:
            nucleus_centriole_split_centriole_df = pd.DataFrame(nucleus_centriole_match_df['Centriole'].to_list(), columns = ['Centriole1', 'Centriole2'], dtype=pd.Int64Dtype())
        except ValueError:
            nucleus_centriole_split_centriole_df = pd.DataFrame(nucleus_centriole_match_df['Centriole'].to_list(), columns = ['Centriole1'], dtype=pd.Int64Dtype())
            nucleus_centriole_split_centriole_df['Centriole2'] = pd.NA

        try:
            nucleus_centriole_split_nc_df = pd.DataFrame(nucleus_centriole_match_df['Nuc_Cent'].to_list(), columns = ['Nuc_Cent1', 'Nuc_Cent2'])
        except ValueError:
            nucleus_centriole_split_nc_df = pd.DataFrame(nucleus_centriole_match_df['Nuc_Cent'].to_list(), columns = ['Nuc_Cent1'])
            nucleus_centriole_split_nc_df['Nuc_Cent2'] = np.nan

        nucleus_centriole_match_df = pd.concat([nucleus_centriole_match_df, nucleus_centriole_split_centriole_df, nucleus_centriole_split_nc_df], axis=1)
        nucleus_centriole_match_df.drop(['Centriole', 'Nuc_Cent'], axis=1, inplace=True)
        nucleus_centriole_match_df.drop_duplicates(inplace=True)

        #endregion

        #region : Nucleus - Cilia Matching
        
        # Match cilia (child) with closest nucleus (parent) 
        nucleus_cilia_match_dict = match(
            parents=nucleus_group.loc[:, coord_fields].values, 
            childs=cilia_group.loc[:, coord_fields].values, 
            arity=1
        )

        # Make df from dict and rename columns
        nucleus_cilia_match_df = pd.DataFrame.from_dict(nucleus_cilia_match_dict, orient='index')
        nucleus_cilia_match_df.rename(columns={"path_length":"Nuc_Cil", "parent":"Nucleus"}, inplace=True)
        nucleus_cilia_match_df.reset_index(inplace=True, names="Cilia")

        # Drop unmatched/invalid cilia
        nucleus_cilia_match_df.drop(nucleus_cilia_match_df[nucleus_cilia_match_df.Nucleus == -1].index, inplace=True)   
        
        # Increment Cilia and Nucleus number since they are 1-based
        nucleus_cilia_match_df["Cilia"] += 1
        nucleus_cilia_match_df["Nucleus"] += 1

        #endregion

        # Merge two matching dataframes
        nucleus_centriole_cilia_df = nucleus_centriole_match_df.merge(right=nucleus_cilia_match_df, how='outer', on=['Nucleus'])

        # Set ImageNumber 
        nucleus_centriole_cilia_df["ImageNumber"] = key

        # Concat in c2c output
        c2c_df = pd.concat([c2c_df, nucleus_centriole_cilia_df], ignore_index=True)

    c2c_type_dict = {'ImageNumber': pd.Int64Dtype(), 'Nucleus': pd.Int64Dtype(), 'Centriole1': pd.Int64Dtype(), 'Centriole2': pd.Int64Dtype(), 'Cilia': pd.Int64Dtype()}
    c2c_df = c2c_df.astype(c2c_type_dict)

    c2c_df["Cent1_Cil"] = c2c_df.apply(lambda x : math.dist(
        [centriole_loc_dict[x["ImageNumber"]][x["Centriole1"]]["Location_Center_X"], centriole_loc_dict[x["ImageNumber"]][x["Centriole1"]]["Location_Center_Y"]], 
        [cilia_loc_dict[x["ImageNumber"]][x["Cilia"]]["Location_Center_X"], cilia_loc_dict[x["ImageNumber"]][x["Cilia"]]["Location_Center_Y"]]
        ) if pd.notna(x["Centriole1"]) and pd.notna(x["Cilia"]) else np.NaN, axis=1)
    c2c_df["Cent2_Cil"] = c2c_df.apply(lambda x : math.dist(
        [centriole_loc_dict[x["ImageNumber"]][x["Centriole2"]]["Location_Center_X"], centriole_loc_dict[x["ImageNumber"]][x["Centriole2"]]["Location_Center_Y"]], 
        [cilia_loc_dict[x["ImageNumber"]][x["Cilia"]]["Location_Center_X"], cilia_loc_dict[x["ImageNumber"]][x["Cilia"]]["Location_Center_Y"]]
        ) if pd.notna(x["Centriole2"]) and pd.notna(x["Cilia"]) else np.NaN, axis=1)
    c2c_df["Cent1_Cent2"] = c2c_df.apply(lambda x : math.dist(
        [centriole_loc_dict[x["ImageNumber"]][x["Centriole1"]]["Location_Center_X"], centriole_loc_dict[x["ImageNumber"]][x["Centriole1"]]["Location_Center_Y"]], 
        [centriole_loc_dict[x["ImageNumber"]][x["Centriole2"]]["Location_Center_X"], centriole_loc_dict[x["ImageNumber"]][x["Centriole2"]]["Location_Center_Y"]]
        ) if pd.notna(x["Centriole1"]) and pd.notna(x["Centriole2"]) else np.NaN, axis=1)
    
    return c2c_df

def append_features(features_df, nucleus_df, centriole_df, cilia_df):

    features_df = features_df.merge(right=nucleus_df.drop(columns=["Location_Center_X", "Location_Center_Y", "Location_Center_Z"]).add_prefix("Nucleus_"), how='left', left_on=['ImageNumber', 'Nucleus'], right_on=['Nucleus_ImageNumber', 'Nucleus_Nucleus'])
    features_df.drop(columns=['Nucleus_ImageNumber', 'Nucleus_Nucleus'], inplace=True)

    features_df = features_df.merge(right=centriole_df.drop(columns=["Location_Center_X", "Location_Center_Y", "Location_Center_Z"]).add_prefix("Centriole1_"), how='left', left_on=['ImageNumber', 'Centriole1'], right_on=['Centriole1_ImageNumber', 'Centriole1_Centriole'])
    features_df.drop(columns=['Centriole1_ImageNumber', 'Centriole1_Centriole'], inplace=True)

    features_df = features_df.merge(right=centriole_df.drop(columns=["Location_Center_X", "Location_Center_Y", "Location_Center_Z"]).add_prefix("Centriole2_"), how='left', left_on=['ImageNumber', 'Centriole2'], right_on=['Centriole2_ImageNumber', 'Centriole2_Centriole'])
    features_df.drop(columns=['Centriole2_ImageNumber', 'Centriole2_Centriole'], inplace=True)

    features_df = features_df.merge(right=cilia_df.drop(columns=["Location_Center_X", "Location_Center_Y", "Location_Center_Z"]).add_prefix("Cilia_"), how='left', left_on=['ImageNumber', 'Cilia'], right_on=['Cilia_ImageNumber', 'Cilia_Cilia'])
    features_df.drop(columns=['Cilia_ImageNumber', 'Cilia_Cilia'], inplace=True)

    features_df.sort_values(by=["ImageNumber", "Cilia"], inplace=True, ignore_index=True)
    return features_df 

def summary_count(c2c_df, nucleus_df, centriole_df, cilia_df):
    nucleus_count_df = nucleus_df[["ImageNumber", "Nucleus"]].groupby("ImageNumber").agg(Total_Nucleus=('Nucleus', 'count'))
    centriole_count_df = centriole_df[["ImageNumber", "Centriole"]].groupby("ImageNumber").agg(Total_Centriole=('Centriole', 'count'))
    cilia_count_df = cilia_df[["ImageNumber", "Cilia"]].groupby("ImageNumber").agg(Total_Cilia=('Cilia', 'count'))
    
    count_df = nucleus_count_df
    count_df = count_df.merge(centriole_count_df, on="ImageNumber")
    count_df = count_df.merge(cilia_count_df, on="ImageNumber")
    
    count_df.reset_index(inplace=True)

    match_count_dict = {}
    grouped_c2c_df =  c2c_df.groupby("ImageNumber")
    for key in grouped_c2c_df.groups.keys():
        group_df = grouped_c2c_df.get_group(key)
        match_count_dict[key] = {}
        match_count_dict[key]["Matched_Nuc_Cent1"] = len(group_df[group_df["Nucleus"].notna() & group_df["Centriole1"].notna() & group_df["Centriole2"].isna() & group_df["Cilia"].isna()])
        match_count_dict[key]["Matched_Nuc_Cent1_Cent2"] = len(group_df[group_df["Nucleus"].notna() & group_df["Centriole1"].notna() & group_df["Centriole2"].notna() & group_df["Cilia"].isna()])
        match_count_dict[key]["Matched_Nuc_Cent1_Cent2_Cil"] = len(group_df[group_df["Nucleus"].notna() & group_df["Centriole1"].notna() & group_df["Centriole2"].notna() & group_df["Cilia"].notna()])
        match_count_dict[key]["Matched_Nuc_Cent1_Cil"] = len(group_df[group_df["Nucleus"].notna() & group_df["Centriole1"].notna() & group_df["Centriole2"].isna() & group_df["Cilia"].notna()])
        match_count_dict[key]["Matched_Nuc_Cil"] = len(group_df[group_df["Nucleus"].notna() & group_df["Centriole1"].isna() & group_df["Centriole2"].isna() & group_df["Cilia"].notna()])
    
    match_count_df = pd.DataFrame.from_dict(match_count_dict, orient='index')
    match_count_df.index.name = "ImageNumber"
    match_count_df.reset_index(inplace=True)

    count_df = count_df.merge(match_count_df, on="ImageNumber")

    return count_df

def plot_mean_per_image(mean_per_image_df, out_path):
    for col in mean_per_image_df.columns:
        if col == "ImageNumber":
            continue
        ax = mean_per_image_df.plot.bar(x="ImageNumber", y=col, title=col, width=1, align="edge")
        plt.savefig(Path(out_path, (col + ".png")))
        plt.close()

if __name__ == "__main__":
    main()