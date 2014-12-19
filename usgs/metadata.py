
import requests
from bs4 import BeautifulSoup

from mapbox.usgs import authentication
from mapbox.usgs import USGSApiKeyRequiredError, EARTH_EXPLORER_CATALOG_NODE
from mapbox.usgs.xml_requests import metadata_request


def get_metadata(scene_id, api_key=None):
    """
    Query the Inventory Service for metadata. Currently only works for Landsat 8 via EarthExplorer.
    """
    
    params = {
        "dataset": "LANDSAT_8",
        "node": EARTH_EXPLORER_CATALOG_NODE,
        "api_key": api_key,
        "scene_id": scene_id
    }
    resp = requests.post("https://earthexplorer.usgs.gov/inventory/soap", metadata_request % params)
    
    xml_data = BeautifulSoup(resp.text)
    items = xml_data.findAll('item')
    
    def get_attributes(item):
        children = item.findChildren()
        keys = map(lambda d: d.name, children)
        values = map(lambda d: d.text, children)
        
        return dict(zip(keys, values))
    
    data = map(get_attributes, items)
    return data

# scene_id = "LC80450332014260LGN00"
# print get_metadata(scene_id)