
import requests
from bs4 import BeautifulSoup

from mapbox.usgs import authentication
from mapbox.usgs.xml_requests import download_options_request


def get_download_options(scene_id, api_key=None):
    """
    Query the Inventory Service for metadata. Currently only works for Landsat 8 via EarthExplorer.
    """
    
    if api_key is None:
        api_key = authentication.login()
    
    params = {
        "dataset": "LANDSAT_8",
        "node": "EE",
        "api_key": api_key,
        "scene_id": scene_id
    }
    resp = requests.post("https://earthexplorer.usgs.gov/inventory/soap", download_options_request % params)
    
    return resp.text