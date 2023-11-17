import pandas as pd
from bisect import insort
from collections import defaultdict
from scipy.spatial import KDTree

def match(parents, childs, arity, thresholds=None):

    kd_tree = KDTree(data=parents, leafsize=10)

    child_to_parent = {}
    visited_child = {}
    parent_to_child = defaultdict(list)

    num_parents = len(parents) + 1 # 1-based for KDTree query

    for child_idx, child_coords in enumerate(childs):

        # Initialize child_to_parent record in dictionary
        child_to_parent[child_idx] = {}
        child_to_parent[child_idx]["path_length"] = float("inf") # The length of the shortest path
        child_to_parent[child_idx]["parent"] = None # The index of the cell to which the shortest path corresponds

        # Record coordinates in visited_child dictionary
        visited_child[child_idx] = child_coords

        # Target child_idx to lookup in KDTree
        lookup_child_idx = child_idx

        for k in range(1, num_parents+1):

            # Query closest parent
            dist_arr, parent_idx_arr = kd_tree.query(x=visited_child[lookup_child_idx], k=[k], workers=1)
            dist = float(dist_arr[0])
            parent_idx = int(parent_idx_arr[0])

            # Get threshold
            if thresholds:
                threshold = 2.5 * thresholds[parent_idx]
            else:
                threshold = float("inf")

            # If closest parent distance is greater than threshold or if missing neighbor (dist is inf), child is automatically invalidated
            if dist > threshold or dist == float("inf"):
                child_to_parent[lookup_child_idx]["path_length"] = -1
                child_to_parent[lookup_child_idx]["parent"] = -1
                break

            # Add parent information to child_to_parent dictionary
            child_to_parent[lookup_child_idx]["path_length"] = dist
            child_to_parent[lookup_child_idx]["parent"] = parent_idx

            # Add child information to parent_to_child dictionary
            insort(parent_to_child[parent_idx], (dist, lookup_child_idx))

            # Check if parent has number of childs exceeding arity
            if len(parent_to_child[parent_idx]) > arity:

                # Remove the furthest child
                _, child_to_remove = parent_to_child[parent_idx].pop()

                # Case of no possible match - no more parents left
                if k == num_parents:
                    child_to_parent[child_to_remove]["path_length"] = -1
                    child_to_parent[child_to_remove]["parent"] = -1
                else: 
                # Proceed to match with next possible closest parent

                    # Reintialize child_to_parent record in dictionary
                    child_to_parent[child_to_remove]["path_length"] = float("inf")
                    child_to_parent[child_to_remove]["parent"] = None

                    # Set removed child as lookup target to match with next available neighbor
                    lookup_child_idx = child_to_remove
            else:
                # If insertion suceed, proceed to next child in list
                break

    return child_to_parent      


def read_cellprofiler_csv(csv_path, organelle):
    cellprofiler_df = pd.read_csv(csv_path, skipinitialspace=True)
    cellprofiler_df = cellprofiler_df.astype({"ImageNumber": pd.Int64Dtype(), "ObjectNumber": pd.Int64Dtype()})
    cellprofiler_df.rename(columns={"ObjectNumber": organelle}, inplace=True)
    return cellprofiler_df