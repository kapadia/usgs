
import os, json

from usgs import api
from usgs import CWIC_LSI_EXPLORER_CATALOG_NODE
from usgs import EARTH_EXPLORER_CATALOG_NODE
from usgs import HDDS_EXPLORER_CATALOG_NODE
from usgs import LPCS_EXPLORER_CATALOG_NODE

scriptdir = os.path.dirname(os.path.abspath(__file__))


def get_datasets_in_nodes():
    """
    Get the node associated with each dataset. Some datasets
    will have an ambiguous node since they exists in more than
    one node.
    """

    data_dir = os.path.join(scriptdir, "..", "usgs", "data")

    cwic = map(lambda d: d["datasetName"], api.datasets(None, CWIC_LSI_EXPLORER_CATALOG_NODE)['data'])
    ee = map(lambda d: d["datasetName"], api.datasets(None, EARTH_EXPLORER_CATALOG_NODE)['data'])
    hdds = map(lambda d: d["datasetName"], api.datasets(None, HDDS_EXPLORER_CATALOG_NODE)['data'])
    lpcs = map(lambda d: d["datasetName"], api.datasets(None, LPCS_EXPLORER_CATALOG_NODE)['data'])

    # Create mapping from dataset to node
    datasets = {}
    datasets.update( { ds : "CWIC" for ds in cwic } )
    datasets.update( { ds : "EE" for ds in ee } )
    datasets.update( { ds : "HDDS" for ds in hdds } )
    datasets.update( { ds : "LPCS" for ds in lpcs } )

    datasets_path = os.path.join(data_dir, "datasets.json")
    with open(datasets_path, "w") as f:
        f.write(json.dumps(datasets))

    # Find the datasets with ambiguous nodes
    cwic_ee = [ds for ds in cwic if ds in ee]
    cwic_hdds = [ds for ds in cwic if ds in hdds]
    cwic_lpcs = [ds for ds in cwic if ds in lpcs]
    ee_hdds = [ds for ds in ee if ds in hdds]
    ee_lpcs = [ds for ds in ee if ds in lpcs]
    hdds_lpcs = [ds for ds in hdds if ds in lpcs]



if __name__ == '__main__':
    get_datasets_in_nodes()