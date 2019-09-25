

import json
import math
from usgs import CATALOG_NODES, USGSDependencyRequired


def clear_bulk_download_order(dataset, node, api_key=None):
    """
    This method is used to clear bulk download order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    raise NotImplementedError


def clear_order(dataset, node, api_key=None):
    """
    This method is used to clear order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    raise NotImplementedError


def dataset_fields(dataset, node, api_key=None):
    """
    This request is used to return the metadata filter
    fields for the specified dataset. These values can
    be used as additional criteria when submitting search
    and hit queries.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is not required.
    """

    return json.dumps({
        "datasetName": dataset,
        "node": node,
        "apiKey": api_key
    })


def datasets(dataset, public_only=False, geojson=None, min_rect=None, start_date=None, end_date=None, api_key=None):
    """
    This method is used to find datasets available for searching.
    By passing no parameters except node, all available datasets
    are returned. Additional parameters such as temporal range
    and spatial bounding box can be used to find datasets that 
    provide more specific data. The dataset name parameter can
    be used to limit the results based on matching the supplied
    value against the dataset name with assumed wildcards at the
    beginning and end. All parameters are optional except for 
    the 'node' parameter.
    
    :param dataset:
        Dataset Identifier
    
    :param ll:
        Lower left corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param ur:
        Upper right corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param start_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param end_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param api_key:
        API key is not required.
        
    """

    payload = {
        "apiKey": api_key,
        "publicOnly": public_only
    }

    if dataset:
        payload["datasetName"] = dataset

    if geojson and min_rect:
        raise Exception("Only one of 'geojson' or 'min_rect' should be specified.")

    if geojson:
        payload["spatialFilter"] = {
            "filterType": "geojson",
            "geeJson": geojson
        }

    if ll and ur:
        payload["spatialFilter"] = {
            "filterType": "mbr",
            "lowerLeft": ll,
            "upperRight": ur
        }

    if start_date and end_date:
        payload["temporalFilter"] = {
            "startDate": start_date,
            "endDate": end_date
        }

    else:
        raise Exception("A `start_date` and `end_date` are both required if one is specified.")

    return json.dumps(payload)


def download(dataset, node, entityids, products, api_key=None):
    """
    The use of this request will be to obtain valid data download URLs.
    
    :param dataset:
    
    :param entityIds:
        list
    
    :param products:
        list
    
    :param node:
    
    :param api_key:
        API key is required.
    """

    payload = {
        "datasetName": dataset,
        "node": node,
        "apiKey": api_key,
        "entityIds": entityids,
        "products": products
    }

    return json.dumps(payload)


def download_options(dataset, node, entityids, api_key=None):
    """
    The use of the download options request is to discover the different download
    options for each scene. Some download options may exist but still be unavailable
    due to disk usage and many other factors. If a download is unavailable
    it may need to be ordered.
    
    :param dataset:
    
    :param node:
    
    :param entityIds:
    
    :param api_key:
        API key is not required.
    """

    payload = {
        "apiKey": api_key,
        "datasetName": dataset,
        "node": node,
        "entityIds": entityids
    }

    return json.dumps(payload)


def get_bulk_download_products(dataset, node, entityids, api_key):
    """
    Retrieve bulk download products on a scene-by-scene basis.

    :param dataset:

    :param node:

    :param entityid:
        String or list of strings.

    :param api_key:
        API key is required.

    """
    raise NotImplementedError


def get_order_products(dataset, node, entityids, api_key=None):
    """
    Retrieve orderable products on a scene-by-scene basis.

    :param dataset:

    :param node:

    :param entityid:

    :param api_key:
        API key is required.

    .. todo:: Support multiple scene request.
    """
    raise NotImplementedError


def item_basket(api_key=None):
    """
    Returns the current item basket for the current user.

    :param api_key:
        API key is required.
    """
    raise NotImplementedError


def login(username, password, catalogId='EE'):
    """
    This method requires SSL be used due to the sensitive nature of
    users passwords. Upon a successful login, an API key will be
    returned. This key will be active for one hour and should be
    destroyed upon final use of the service by calling the logout
    method. Users must have "Machine to Machine" access based on
    a user-based role in the users profile.
    
    :param username:
    
    :param password:
    """

    payload = {
        "username": username,
        "password": password,
        "authType": "",
        "catalogId": catalogId
    }

    return json.dumps(payload)


def logout(api_key):
    """
    Remove the users API key from being used in the future.
    
    :param api_key:
        API key is required.
    """

    payload = {
        "apiKey": api_key
    }
    return json.dumps(payload)


def metadata(dataset, node, entityids, api_key=None):
    """
    The use of the metadata request is intended for those who have
    acquired scene IDs from a different source. It will return the
    same metadata that is available via the search request.
    
    :param dataset:
    
    :param node:
    
    :param sceneid:
    
    :param api_key:
    """

    payload = {
        "apiKey": api_key,
        "datasetName": dataset,
        "node": node,
        "entityIds": entityids
    }

    return json.dumps(payload)


def remove_bulk_download_scene():
    raise NotImplementedError


def remove_order_scene():
    raise NotImplementedError


def great_circle_dist(lat, lng, dist):
    lat = math.radians(lat)
    lng = math.radians(lng)
    brng = math.radians(45.0)
    ibrng = math.radians(225.0)

    earth_radius = 6371000.0
    dR = (dist / 2.0)/ earth_radius

    lat1 = math.asin( math.sin(lat)*math.cos(dR) +
        math.cos(lat)*math.sin(dR)*math.cos(brng) );
    lng1 = lng + math.atan2(math.sin(brng)*math.sin(dR)*math.cos(lat),
        math.cos(dR)-math.sin(lat)*math.sin(lat1));

    lat2 = math.asin( math.sin(lat)*math.cos(dR) +
        math.cos(lat)*math.sin(dR)*math.cos(ibrng) );
    lng2 = lng + math.atan2(math.sin(ibrng)*math.sin(dR)*math.cos(lat),
        math.cos(dR)-math.sin(lat)*math.sin(lat2));

    return [math.degrees(lat1), math.degrees(lat2)], [math.degrees(lng1), math.degrees(lng2)]


def search(dataset, node, geojson=None,
    lat=None, lng=None,
    distance=100,
    ll=None, ur=None,
    start_date=None, end_date=None,
    where=None,
    max_results=50000,
    starting_number=1,
    sort_order="DESC",
    api_key=None):
    """
    :param dataset:
    
    :param node:
    
    :param lat:
    
    :param lng:
    
    :param ll:
    
    :param distance:
    
    :param ur:
    
    :param start_date:
    
    :param end_date:
    
    :param where:
        Specify additional search criteria
    
    :param max_results:
    
    :param starting_number:
    
    :param sort_order:
    
    :param api_key:
        API key is not required.
    """

    payload = {
        "datasetName": dataset,
        "node": node,
        "apiKey": api_key,
    }

    if geojson and (ll and ur) or geojson and (lat and lng):
        raise Exception("Only one of 'geojson' or `ll` and `ur` or `lat` and `lng` should be specified.")

    if geojson:
        payload["spatialFilter"] = {
            "filterType": "geojson",
            "geeJson": geojson
        }
    else:
        # Latitude and longitude take precedence over ll and ur
        if lat and lng:

            lats, lngs = great_circle_dist(lat, lng, distance / 2.0)

            ll = { "longitude": min(*lngs), "latitude": min(*lats) }
            ur = { "longitude": max(*lngs), "latitude": max(*lats) }

        if ll and ur:
            payload["spatialFilter"] = {
                "filterType": "mbr",
                "lowerLeft": ll,
                "upperRight": ur
            }

    if start_date or end_date:
        payload["temporalFilter"] = {
            "dateField": "search_date"
        }

        if start_date:
            payload["temporalFilter"]["startDate"] = start_date
        if end_date:
            payload["temporalFilter"]["endDate"] = end_date

    if where:

        # TODO: Support more than AND key/value equality queries
        # usgs search --node EE LANDSAT_8_C1 --start-date 20170410 --end-date 20170411 --where wrs-row 032 | jq ""
        # LC81810322017101LGN00
        payload["additionalCriteria"] = {
            "filterType": "and",
            "childFilters": [
                {
                    "filterType": "value",
                    "fieldId": field_id,
                    "value": value,
                    "operand": "="
                }
                for field_id, value in iter(where.items())
            ]
        }

    if max_results:
        payload["maxResults"] = max_results

    if starting_number:
        payload["startingNumber"] = starting_number

    if sort_order:
        payload["sortOrder"] = sort_order

    return json.dumps(payload)


def submit_bulk_order():
    raise NotImplementedError


def submit_order():
    raise NotImplementedError


def update_bulk_download_scene():
    raise NotImplementedError


def update_order_scene():
    raise NotImplementedError
