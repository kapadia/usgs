
import os, json

from usgs import api
from usgs import CWIC_LSI_EXPLORER_CATALOG_NODE
from usgs import EARTH_EXPLORER_CATALOG_NODE
from usgs import HDDS_EXPLORER_CATALOG_NODE
from usgs import LPVS_EXPLORER_CATALOG_NODE


def get_datasets_in_nodes():
    """
    Get the node associated with each dataset. Some datasets
    will have an ambiguous node since they exists in more than
    one node.
    """
    
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(cur_dir, "..", "data")
    
    cwic = map(lambda d: d["datasetName"], api.datasets(None, CWIC_LSI_EXPLORER_CATALOG_NODE))
    ee = map(lambda d: d["datasetName"], api.datasets(None, EARTH_EXPLORER_CATALOG_NODE))
    hdds = map(lambda d: d["datasetName"], api.datasets(None, HDDS_EXPLORER_CATALOG_NODE))
    lpvs = map(lambda d: d["datasetName"], api.datasets(None, LPVS_EXPLORER_CATALOG_NODE))
    
    # Create mapping from dataset to node
    datasets = {}
    datasets.update( { ds : "cwic" for ds in cwic } )
    datasets.update( { ds : "ee" for ds in ee } )
    datasets.update( { ds : "hdds" for ds in hdds } )
    datasets.update( { ds : "lpvs" for ds in lpvs } )
    
    datasets_path = os.path.join(data_dir, "datasets.json")
    with open(datasets_path, "w") as f:
        f.write(json.dumps(datasets))
    
    # Luckily there are only four nodes.
    
    # Find the datasets with ambiguous nodes
    cwic_ee = [ds for ds in cwic if ds in ee]
    cwic_hdds = [ds for ds in cwic if ds in hdds]
    cwic_lpvs = [ds for ds in cwic if ds in lpvs]
    
    ee_hdds = [ds for ds in ee if ds in hdds]
    ee_lpvs = [ds for ds in ee if ds in lpvs]
    
    hdds_lpvs = [ds for ds in hdds if ds in lpvs]
    


if __name__ == '__main__':
    get_datasets_in_nodes()