import pandas as pd
from math import sqrt, isnan
from pandas.core.frame import DataFrame
from collections import defaultdict
from bisect import insort
from scipy.spatial import KDTree
import argparse
import os

def make_lists(im_num, grouped):
    """
    Group dataframe into only rows where image is im_num and return the values in a list

    :param im_num: The image number
    :param grouped: The dataframe we want to get relevant rows of
    :returns: List of (x,y) coordinates for all relevant rows of dataframe
    """

    im_df = (grouped.get_group(im_num)).copy()
    im_df.drop("ImageNumber", axis=1, inplace=True)
    return im_df.values.tolist()


def nearest_child(parent_list, child_list, arity, threshold=float("inf")):
    """
    Find nearest child for each parent
    :param parent_list: List of parent coordinates
    :param child_list: List of child coordinates
    :param arity: How many children each parent can have
    :param threshold: Distance threshold from parent to child
    :returns: List of child pairs, List of children without parent
    """

    kd_tree = KDTree(parent_list)
    child_to_parent = [
        {
            "path_length": float("inf"),  # The length of the shortest path
            "parent": None,  # The index of the cell to which the shortest path corresponds
        }
        for _ in child_list
    ]

    visited = defaultdict(list)
    removed = set()

    for child_idx, child_coords in enumerate(child_list):
        dist, parent_idx = kd_tree.query(child_coords)
        parent_idx = parent_idx + 1

        if dist > threshold:
            child_to_parent[child_idx]["path_length"] = -1
            child_to_parent[child_idx]["parent"] = -1
            continue

        child_to_parent[child_idx]["path_length"] = dist
        child_to_parent[child_idx]["parent"] = parent_idx

        insort(visited[parent_idx], (dist, child_idx))
        if len(visited[parent_idx]) > arity:

            _, child_to_remove = visited[parent_idx].pop()

            child_to_parent[child_to_remove]["path_length"] = -1
            child_to_parent[child_to_remove]["parent"] = -1
            removed.add(child_to_remove)

    return child_to_parent, removed


def convert_dict_to_csv(c2c_output, output_path):
    """
    Convert our output into a csv

    :param c2c_output: Output to store
    :param output_path: Path to store output to
    :returns: None
    """

    df = pd.DataFrame.from_dict(c2c_output)
    df = df.dropna()
    cols = df.columns.tolist()
    df = df[
        [
            "num",
            "cell",
            "path_length_centrioles",
            "centrioles",
            "path_length_cilia",
            "cilia",
        ]
    ]
    df.to_csv(
        path_or_buf=output_path,
        header=[
            "ImageNumber",
            "Nucleus",
            "PathLengthCentriole",
            "Centriole",
            "PathLengthCilia",
            "Cilia",
        ],
        index=False,
        float_format="%.10g",
    )


def combine_lists(centriole_to_cell, cilia_to_cell, num, cell_list):
    """
    Combine the cell/centriole and cell/cilia lists to make one unified dictionary

    :param centriole_to_cell: List of centrioles and cells they attach to
    :param cilia_to_cell: List of cilia and cells they attach to
    :param num: Image number
    :param cell_list: List of cells to initialize output with
    :returns: List of properly formatted output
    """

    c2c_output_formatted = [
        {
            "num": num,
            "cell": cell,
            "centrioles": [],
            "path_length_centrioles": [],
            "path_length_cilia": float("inf"),
            "cilia": None,
        }
        for cell in range(len(cell_list) + 1)
    ]

    for x, cell_dict in enumerate(centriole_to_cell):
        if cell_dict["path_length"] == -1:
            continue
        cent = x + 1
        cell_to_add_to = cell_dict["parent"]
        path_to_add_to = cell_dict["path_length"]
        c2c_output_formatted[cell_to_add_to]["centrioles"].append(cent)
        c2c_output_formatted[cell_to_add_to]["path_length_centrioles"].append(
            path_to_add_to
        )

    for x, cell_dict in enumerate(cilia_to_cell):
        if cell_dict["path_length"] == -1:
            continue
        cilia = x + 1
        cell_to_add_to = cell_dict["parent"]
        path_to_add_to = cell_dict["path_length"]
        c2c_output_formatted[cell_to_add_to]["cilia"] = cilia
        c2c_output_formatted[cell_to_add_to]["path_length_cilia"] = path_to_add_to

    return c2c_output_formatted


def remove_noise(x_list, noise_list, num):
    """
    Make a list of indices of x list that are attached to some y

    :param x_list: List of coordinates for each x
    :param noise_list: Noise indices to get rid of
    :param num: Image number
    :returns: List of x that only has the x that have been paired, List of indices with invalid centrioles skipped
    """

    valid_list = []
    true_idx_mapping = []
    for idx, cur_x in enumerate(x_list):
        if idx not in noise_list:
            valid_list.append(cur_x)
            true_idx_mapping.append([num, idx])

    return valid_list, true_idx_mapping


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
        "-o", "--output", help="output folder path", required=True
    )
    
    return vars(parser.parse_args())


def main(**args):

    args = args or parse_args()

    ### Make output path if not exist

    center2center_output_path = os.path.join(args["output"], "center2center_output")

    if not os.path.exists(center2center_output_path):
        os.mkdir(center2center_output_path)

    ### Reading CSVS and filtering fields

    # Fields to filter
    fields = ["ImageNumber", "Location_Center_X", "Location_Center_Y"]

    # Read filtered fields of nucleus csv into a dataframe
    cell_df = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Nucleus.csv"), skipinitialspace=True, usecols=fields
    )

    # Get total number of images by reading the last ImageNumber entry from dataframe
    num_im = cell_df.ImageNumber.iat[-1]

    # Group rows by ImageNumber
    grouped_cell = cell_df.groupby(["ImageNumber"])

    # Read filtered fields of centriole csv into a dataframe
    centriole_df = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Centriole.csv"), skipinitialspace=True, usecols=fields
    )
    # Group rows by Image number
    grouped_centriole = centriole_df.groupby(["ImageNumber"])
    
    # Read filtered fields of cilia csv into a dataframe
    cilia_df = pd.read_csv(
        os.path.join(args["measurements"], "MyExpt_Cilia.csv"), skipinitialspace=True, usecols=fields
    )
    # Group rows by Image number
    grouped_cilia = cilia_df.groupby(["ImageNumber"])

    # Make lists for the output
    c2c_output = []
    valid_cilia = []
    valid_cent = []

    # Iterate over each ImageNumber
    for num in range(1, num_im + 1):
        # Convert groupby objects to list for easy access
        cell_list = make_lists(num, grouped_cell)
        centriole_list = make_lists(num, grouped_centriole)
        cilia_list = make_lists(num, grouped_cilia)

        # Match centrioles to cell (nuclei)
        centriole_to_cell, cent_to_remove = nearest_child(cell_list, centriole_list, 2)

        # Make list of valid cent
        _, valid_cent_indices = remove_noise(centriole_list, cent_to_remove, num)
        valid_cent_indices = [[idx[0], (idx[1] + 1)] for idx in valid_cent_indices]
        valid_cent += valid_cent_indices

        # Match cilia to cell
        cilia_to_cell, cilia_to_remove = nearest_child(cell_list, cilia_list, 1)

        # Make list of valid cilia
        _, valid_cilia_indices = remove_noise(cilia_list, cilia_to_remove, num)
        valid_cilia_indices = [[idx[0], (idx[1] + 1)] for idx in valid_cilia_indices]
        valid_cilia += valid_cilia_indices

        # Combine the two match lists and add to the list of all output 
        c2c_formatted = combine_lists(centriole_to_cell, cilia_to_cell, num, cell_list)
        c2c_output += c2c_formatted

    # Finally, output valid lists and pairing list as csv
    valid_cent_df = pd.DataFrame(valid_cent)
    valid_cilia_df = pd.DataFrame(valid_cilia)

    convert_dict_to_csv(c2c_output, os.path.join(center2center_output_path, "c2c_output.csv"))
    valid_cent_df.to_csv(os.path.join(center2center_output_path, "new_cent.csv"))
    valid_cilia_df.to_csv(os.path.join(center2center_output_path, "new_cilia.csv"))

    return center2center_output_path


if __name__ == "__main__":
    main()

