import json
import math
from collections import defaultdict
from usgs import CATALOG_NODES, USGSDependencyRequired


def dataset_filters(dataset):
    """
    This request is used to return the metadata filter fields for the specified
    dataset. These values can be used as additional criteria when submitting search
    and hit queries.

    :param str dataset:
    """
    return json.dumps({
        "datasetName": dataset,
    })

def download_options(dataset, entity_ids):
    """
    The download options request is used to discover downloadable products for
    each dataset. If a download is marked as not available, an order must be
    placed to generate that product.

    :param str dataset:
    :param str entity_ids:
    """

    payload = {
        "datasetName": dataset,
        "entityIds": entity_ids
    }

    return json.dumps(payload)

def download_request(dataset, entity_id, product_id):
    """
    The use of this request will be to obtain valid data download URLs.

    :param str dataset:
    :param str entity_id:
    :param str product_id:
    """

    payload = {
        "downloads": [
            {
                "entityId": entity_id,
                "productId": product_id
            }
        ],
        "downloadApplication": "EE"
    }

    return json.dumps(payload)

def dataset_search(dataset, catalog, start_date=None, end_date=None, ll=None, ur=None):
    """
    This method is used to find datasets available for searching. By passing only
    an API Key, all available datasets are returned. Additional parameters such
    as temporal range and spatial bounding box can be used to find datasets that
    provide more specific data. The dataset name parameter can be used to limit
    the results based on matching the supplied value against the public dataset
    name with assumed wildcards at the beginning and end.

    :param str dataset:
    :param str catalog:
    :param start_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand

    :param end_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand

    :param ll:
        Lower left corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary

        e.g. { "longitude": 0.0, "latitude": 0.0 }

    :param ur:
        Upper right corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary

        e.g. { "longitude": 0.0, "latitude": 0.0 }
    """

    payload = {
        "datasetName": dataset,
        "catalog": catalog
    }

    if start_date and end_date:
        payload["temporalFilter"] = {
            "start": start_date,
            "end": end_date
        }

    if ll and ur:
        payload["spatialFilter"] = {
            "filterType": "mbr",
            "lowerLeft": {
                "latitude": ll["latitude"],
                "longitude": ll["longitude"]
            },
            "upperRight": {
                "latitude": ur["latitude"],
                "longitude": ur["longitude"]
            }
        }

    return json.dumps(payload)

def login(username, password):
    """
    Upon a successful login, an API key will be returned. This key will be active
    for two hours and should be destroyed upon final use of the service by calling
    the logout method.

    :param str username:
    :param str password:
    """
    payload = {
        "username": username,
        "password": password
    }

    return json.dumps(payload)


def scene_metadata(dataset, entity_id):
    """
    The use of the metadata request is intended for those who have
    acquired scene IDs from a different source. It will return the
    same metadata that is available via the search request.

    :param dataset:
    :param entity_id:
    """
    payload = {
        "datasetName": dataset,
        "entityId": entity_id,
        "metadataType": "full"
    }

    return json.dumps(payload)


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

def scene_search(
    dataset, max_results=None, metadata_type=None, start_date=None,
    end_date=None, ll=None, ur=None,
    lat=None, lng=None, distance=100,
    where=None, starting_number=None):

    payload = defaultdict(dict, {
        "datasetName": dataset,
        "maxResults": max_results,
        "startingNumber": starting_number,
        "metadata_type": metadata_type
    })

    if (start_date is not None) and (end_date is not None):
        payload["sceneFilter"]["acquisitionFilter"] = {
            "start": start_date,
            "end": end_date
        }

    # Latitude and longitude take precedence over ll and ur
    if lat and lng:
        lats, lngs = great_circle_dist(lat, lng, distance / 2.0)

        ll = { "longitude": min(*lngs), "latitude": min(*lats) }
        ur = { "longitude": max(*lngs), "latitude": max(*lats) }

    if ll and ur:
        payload["sceneFilter"]["spatialFilter"] = {
            "filterType": "mbr",
            "lowerLeft": ll,
            "upperRight": ur
        }

    if where:
        payload["sceneFilter"]["metadataFilter"] = {
            "filterType": "value",
            "filterId": where["filter_id"],
            "value": where["value"],
            "operand": "="
        }

    return json.dumps(payload)
