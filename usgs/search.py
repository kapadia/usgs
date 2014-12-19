
import re
import math
import requests
import pyproj
from shapely.geometry import box
from bs4 import BeautifulSoup

from mapbox.usgs import endpoint, authentication
from mapbox.usgs import USGSApiKeyRequiredError, EARTH_EXPLORER_CATALOG_NODE
from mapbox.usgs.xml_requests import search_request, lower_left_search, upper_right_search, start_date_search, end_date_search


def get_scenes(
        longitude=None,
        latitude=None,
        distance=100,
        start_date=None,
        end_date=None,
        api_key=None,
        dataset="LANDSAT_8"
    ):
    """
    Query the Inventory Service for scenes within a given start and end date.
    
    .. todo:: Validate dates
    """
    retries = 5
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    params = {
        "dataset": dataset,
        "node": EARTH_EXPLORER_CATALOG_NODE,
        "api_key": api_key,
    }
    
    # Add the search parameters into the request
    xml_request = BeautifulSoup(search_request % params, "xml")
    search_tag = xml_request.find("search")
    
    if longitude and latitude:
        
        prj = pyproj.Proj(proj='aeqd', lat_0=latitude, lon_0=longitude)
    
        half_distance = 0.5 * distance
        b = box(-half_distance, -half_distance, half_distance, half_distance)
        lngs, lats = map(list, prj(*b.exterior.xy, inverse=True))
        
        coordinates = {
            "lat_ll": lats[0], "lng_ll": lngs[0],
            "lat_ur": lats[2], "lng_ur": lngs[2]
        }
        
        ll = BeautifulSoup(lower_left_search % coordinates, "xml")
        ur = BeautifulSoup(upper_right_search % coordinates, "xml")
        search_tag.append(ll.children.next())
        search_tag.append(ur.children.next())
        
    if start_date:

        date = {"start_date": start_date}
        bs = BeautifulSoup(start_date_search % date, "xml")
        search_tag.append(bs.children.next())

    if end_date:

        date = {"end_date": end_date}
        bs = BeautifulSoup(end_date_search % date, "xml")
        search_tag.append(bs.children.next())
    
    for attempt in range(retries, 0, -1):
        if attempt != retries:
            time.sleep(10)
        try:
            resp = requests.post(endpoint, data=str(xml_request))
            break
        except:
            pass
    
    xml_data = BeautifulSoup(resp.text.strip(), "xml")
    items = xml_data.findAll('item')
    
    def get_field(item):
        """
        Parse a single field from one item of the search results
        e.g. acquisitionDate, lowerLeftCoordinate
        """
        key = item.name
    
        children = item.findChildren()
        if children:
            fields = map(get_field, children)
            value = {field[0]: field[1] for field in fields}
        else:
            value = item.text
    
        return [key, value]
    
    def get_attributes(item):
        children = item.findChildren()
        fields = map(get_field, children)
    
        return {field[0]: field[1] for field in fields}
    
    def get_path_row(summary):
        """Parse the Path/Row from the summary field. So much for structured data ..."""
        path_match = re.search("Path:\s*(\d+)", summary)
        row_match = re.search("Row:\s*(\d+)", summary)
        
        return {
            "path": path_match.group(1),
            "row": row_match.group(1)
        }
    
    data = map(get_attributes, items)
    for datum in data:
        pr = get_path_row(datum["summary"])
        datum.update(pr)
    
    return data
