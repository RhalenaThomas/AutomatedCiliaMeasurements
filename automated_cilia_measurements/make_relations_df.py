import pandas as pd
import numpy as np
import argparse
import os


def split_centriole_col(c2c_pairings):
    """
    Split centrioles into two columns

    :param c2c_pairings: Dataframe of just pairings
    :returns: Pairing dataframe with split centrioles
    """
    c2c_pairings["Centriole"] = (
        c2c_pairings["Centriole"].fillna("[]").apply(lambda x: eval(x))
    )
    c2c_pairings["PathLengthCentriole"] = (
        c2c_pairings["PathLengthCentriole"].fillna("[]").apply(lambda x: eval(x))
    )

    # Edit c2c data to separate centrioles into two columns
    split_df = pd.DataFrame(
        c2c_pairings["Centriole"].to_list(), columns=["Cent1", "Cent2"]
    )
    split_df_2 = pd.DataFrame(
        c2c_pairings["PathLengthCentriole"].to_list(),
        columns=["PathCent1", "PathCent2"],
    )
    c2c_pairings = pd.concat([c2c_pairings, split_df], axis=1)
    c2c_pairings = pd.concat([c2c_pairings, split_df_2], axis=1)
    c2c_pairings = c2c_pairings.drop(["Centriole", "PathLengthCentriole"], axis=1)

    # Set up the K-Means/scaling/PCA for visualization

    return c2c_pairings


def normalize_and_clean(
    measurements_nuc, measurements_cilia, measurements_cent, c2c_pairings
):
    """
    Merge dataframes together and add columns to the newly-created full dataframe

    :param measurements_nuc: Dataframe of nuclei measurements
    :param measurements_cilia: Dataframe of cilia measurements
    :param measurements_cent: Dataframe of centriole measurements
    :param c2c_pairings: Dataframe of all pairings betwen nuclei, cilia, and centrioles
    :returns: Merged dataframe
    """
    # Prepare to merge
    measurements_nuc = measurements_nuc.rename(
        columns={
            "ObjectNumber": "Nucleus",
            "AreaShape_Area": "NucArea",
            "AreaShape_Compactness": "NucCompactness",
            "AreaShape_Eccentricity": "NucEccentricity",
            "AreaShape_EquivalentDiameter": "NucEquivDiameter",
            "AreaShape_EulerNumber": "NucEulerNum",
            "AreaShape_Extent": "NucExtent",
            "AreaShape_FormFactor": "NucFormFactor",
            "AreaShape_MajorAxisLength": "NucMajorAxisLength",
            "AreaShape_MaxFeretDiameter": "NucMaxFeretDiameter",
            "AreaShape_MaximumRadius": "NucMaxRadius",
            "AreaShape_MeanRadius": "NucMeanRadius",
            "AreaShape_MedianRadius": "NucMedianRadius",
            "AreaShape_MinFeretDiameter": "NucMinFeretDiameter",
            "AreaShape_MinorAxisLength": "NucMinorAxisLength",
            "AreaShape_Orientation": "NucOrientation",
            "AreaShape_Perimeter": "NucPerimeter",
            "AreaShape_Solidity": "NucSolidity",
            "Location_Center_X": "NucX",
            "Location_Center_Y": "NucY",
        }
    )

    measurements_cilia = measurements_cilia.rename(
        columns={
            "ObjectNumber": "Cilia",
            "AreaShape_Area": "CiliaArea",
            "AreaShape_Compactness": "CiliaCompactness",
            "AreaShape_Eccentricity": "CiliaEccentricity",
            "AreaShape_EquivalentDiameter": "CiliaEquivDiameter",
            "AreaShape_EulerNumber": "CiliaEulerNum",
            "AreaShape_Extent": "CiliaExtent",
            "AreaShape_FormFactor": "CiliaFormFactor",
            "AreaShape_MajorAxisLength": "CiliaMajorAxisLength",
            "AreaShape_MaxFeretDiameter": "CiliaMaxFeretDiameter",
            "AreaShape_MaximumRadius": "CiliaMaxRadius",
            "AreaShape_MeanRadius": "CiliaMeanRadius",
            "AreaShape_MedianRadius": "CiliaMedianRadius",
            "AreaShape_MinFeretDiameter": "CiliaMinFeretDiameter",
            "AreaShape_MinorAxisLength": "CiliaMinorAxisLength",
            "AreaShape_Orientation": "CiliaOrientation",
            "AreaShape_Perimeter": "CiliaPerimeter",
            "AreaShape_Solidity": "CiliaSolidity",
            "Location_Center_X": "CiliaX",
            "Location_Center_Y": "CiliaY",
        }
    )

    measurements_cent_1 = measurements_cent.rename(
        columns={
            "ObjectNumber": "Cent1",
            "AreaShape_Area": "CentArea1",
            "AreaShape_Compactness": "CentCompactness1",
            "AreaShape_Eccentricity": "CentEccentricity1",
            "AreaShape_EquivalentDiameter": "CentEquivDiameter1",
            "AreaShape_EulerNumber": "CentEulerNum1",
            "AreaShape_Extent": "CentExtent1",
            "AreaShape_FormFactor": "CentFormFactor1",
            "AreaShape_MajorAxisLength": "CentMajorAxisLength1",
            "AreaShape_MaxFeretDiameter": "CentMaxFeretDiameter1",
            "AreaShape_MaximumRadius": "CentMaxRadius1",
            "AreaShape_MeanRadius": "CentMeanRadius1",
            "AreaShape_MedianRadius": "CentMedianRadius1",
            "AreaShape_MinFeretDiameter": "CentMinFeretDiameter1",
            "AreaShape_MinorAxisLength": "CentMinorAxisLength1",
            "AreaShape_Orientation": "CentOrientation1",
            "AreaShape_Perimeter": "CentPerimeter1",
            "AreaShape_Solidity": "CentSolidity1",
            "Location_Center_X": "CentX1",
            "Location_Center_Y": "CentY1",
        }
    )
    measurements_cent_2 = measurements_cent.rename(
        columns={
            "ObjectNumber": "Cent2",
            "AreaShape_Area": "CentArea2",
            "AreaShape_Compactness": "CentCompactness2",
            "AreaShape_Eccentricity": "CentEccentricity2",
            "AreaShape_EquivalentDiameter": "CentEquivDiameter2",
            "AreaShape_EulerNumber": "CentEulerNum2",
            "AreaShape_Extent": "CentExtent2",
            "AreaShape_FormFactor": "CentFormFactor2",
            "AreaShape_MajorAxisLength": "CentMajorAxisLength2",
            "AreaShape_MaxFeretDiameter": "CentMaxFeretDiameter2",
            "AreaShape_MaximumRadius": "CentMaxRadius2",
            "AreaShape_MeanRadius": "CentMeanRadius2",
            "AreaShape_MedianRadius": "CentMedianRadius2",
            "AreaShape_MinFeretDiameter": "CentMinFeretDiameter2",
            "AreaShape_MinorAxisLength": "CentMinorAxisLength2",
            "AreaShape_Orientation": "CentOrientation2",
            "AreaShape_Perimeter": "CentPerimeter2",
            "AreaShape_Solidity": "CentSolidity2",
            "Location_Center_X": "CentX2",
            "Location_Center_Y": "CentY2",
        }
    )

    # Merge so we get the list of all measurements we desire
    full_df = c2c_pairings.merge(measurements_cilia, on=["ImageNumber", "Cilia"])
    full_df = full_df.merge(measurements_nuc, on=["ImageNumber", "Nucleus"])

    cent1_na = full_df[full_df["Cent1"].isna()]
    full_df = full_df.merge(measurements_cent_1, on=["ImageNumber", "Cent1"])
    full_df = pd.concat([full_df, cent1_na], ignore_index=True)

    cent2_na = full_df[full_df["Cent2"].isnull()]
    full_df = full_df.merge(measurements_cent_2, on=["ImageNumber", "Cent2"])
    full_df = pd.concat([full_df, cent2_na], ignore_index=True)


    # Add binary cols and distance cols
    full_df["CiliaCent1"] = np.where(
        full_df["Cent1"].isnull(),
        0,
        (
            ((full_df["CentX1"] - full_df["CiliaX"]) ** 2)
            + ((full_df["CentY1"] - full_df["CiliaY"]) ** 2)
        )
        ** (1 / 2),
    )
    full_df["CiliaCent2"] = np.where(
        full_df["Cent2"].isnull(),
        0,
        (
            ((full_df["CentX2"] - full_df["CiliaX"]) ** 2)
            + ((full_df["CentY2"] - full_df["CiliaY"]) ** 2)
        )
        ** (1 / 2),
    )

    full_df["Cent1Bin"] = np.where(full_df["Cent1"].isnull(), 0, 1)
    full_df["Cent2Bin"] = np.where(full_df["Cent2"].isnull(), 0, 1)

    full_df.fillna(0, inplace=True)


    return full_df


def parse_args():
    """
    Parse passed in arguments

    :returns: Necessary arguments to use the script
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-m", "--measurements", help="path to directory with CellProfiler CSVs", required=True
    )

    parser.add_argument(
        "-c", "--c2c", help="path to directory with c2c CSV", required=True
    )

    parser.add_argument(
        "-o", "--output", help="output folder to save relations df to", required=True,
    )

    return vars(parser.parse_args())


def main(**args):

    args = args or parse_args()

    make_relations_df_output_path = os.path.join(args["output"], "make_relations_df_output")
    
    if not os.path.exists(make_relations_df_output_path):
        os.mkdir(make_relations_df_output_path)

    fields = [
        "ImageNumber",
        "ObjectNumber",
        "AreaShape_Area",
        "AreaShape_Compactness",
        "AreaShape_Eccentricity",
        "AreaShape_EquivalentDiameter",
        "AreaShape_EulerNumber",
        "AreaShape_Extent",
        "AreaShape_FormFactor",
        "AreaShape_MajorAxisLength",
        "AreaShape_MaxFeretDiameter",
        "AreaShape_MaximumRadius",
        "AreaShape_MeanRadius",
        "AreaShape_MedianRadius",
        "AreaShape_MinFeretDiameter",
        "AreaShape_MinorAxisLength",
        "AreaShape_Orientation",
        "AreaShape_Perimeter",
        "AreaShape_Solidity",
        "Location_Center_X",
        "Location_Center_Y",
    ]

    # Convert the CSVs into dataframes and group by image
    measurements_cilia = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Cilia.csv"),
        skipinitialspace=True,
        usecols=fields,
    )

    measurements_nuc = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Nucleus.csv"),
        skipinitialspace=True,
        usecols=fields,
    )

    measurements_cent = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Centriole.csv"),
        skipinitialspace=True,
        usecols=fields,
    )

    c2c_pairings = pd.read_csv(
        os.path.join(args["c2c"], "c2c_output.csv"),
        skipinitialspace=True
    )

    c2c_pairings = split_centriole_col(c2c_pairings)

    full_df = normalize_and_clean(
        measurements_nuc, measurements_cilia, measurements_cent, c2c_pairings
    )
    
    full_df.to_csv(os.path.join(make_relations_df_output_path, "rel_and_attr_df.csv"))

    return make_relations_df_output_path


if __name__ == "__main__":
    main()
