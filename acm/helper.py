from bisect import insort
from collections import defaultdict
from scipy.spatial import KDTree

def match(data, lookups, arity=1, threshold=float('inf')):
    
    # Initialize KDTree, based on parents array of coordinates
    # Set leafsize to 2, for better lookup performance
    tree = KDTree(data, leafsize=2)

    distances, idxs = tree.query(x=lookups, k=arity, distance_upper_bound=threshold)

    return distances, idxs        


