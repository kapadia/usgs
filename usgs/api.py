
import os
from os.path import expanduser
from xml.etree import ElementTree
import requests
from requests_futures.sessions import FuturesSession

from usgs import USGS_API, USGSError
from usgs import xsi, payloads


TMPFILE = os.path.join(expanduser("~"), ".usgs")
NAMESPACES = {
    "eemetadata": "http://earthexplorer.usgs.gov/eemetadata.xsd"
}


def _get_api_key(api_key):

    if api_key is None and os.path.exists(TMPFILE):
        with open(TMPFILE, "r") as f:
            api_key = f.read()

    return api_key


def _check_for_usgs_error(data):

    error_code = data['errorCode']
    if error_code is None:
        return

    error = data['error']

    raise USGSError('%s: %s' % (error_code, error))


def _get_extended(scene, resp):
    """
    Parse metadata returned from the metadataUrl of a USGS scene.

    :param scene:
        Dictionary representation of a USGS scene
    :param resp:
        Response object from requests/grequests
    """
    root = ElementTree.fromstring(resp.text)
    items = root.findall("eemetadata:metadataFields/eemetadata:metadataField", NAMESPACES)
    scene['extended'] = {item.attrib.get('name').strip(): xsi.get(item[0]) for item in items}

    return scene


def _async_requests(urls):
    """
    Sends multiple non-blocking requests. Returns
    a list of responses.

    :param urls:
        List of urls
    """
    session = FuturesSession(max_workers=30)
    futures = [
        session.get(url)
        for url in urls
    ]
    return [ future.result() for future in futures ]


def _get_metadata_url(scene):
    return scene['metadataUrl']


def clear_bulk_download_order():
    raise NotImplementedError


def clear_order():
    raise NotImplementedError


def dataset_fields(dataset, node, api_key=None):

    api_key = _get_api_key(api_key)

    payload = {
        "jsonRequest": payloads.dataset_fields(dataset, node, api_key=api_key)
    }
    url = '{}/datasetfields'.format(USGS_API)
    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    return response


def datasets(dataset, node, ll=None, ur=None, start_date=None, end_date=None, api_key=None):

    api_key = _get_api_key(api_key)

    url = '{}/datasets'.format(USGS_API)

    payload = {
        "jsonRequest": payloads.datasets(dataset, node, ll=ll, ur=ur, start_date=start_date, end_date=end_date, api_key=api_key)
    }
    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    return response


def download(dataset, node, entityids, product='STANDARD', api_key=None):
    """
    Though USGS supports multiple products in a single request, there's
    ambiguity in the returned list. This wrapper only allows a single
    product per request.

    Additionally, the response has no indiction which URL is associated
    with which scene/entity id. The URL can be parsed, but the structure
    varies depending on the product.
    """

    api_key = _get_api_key(api_key)

    url = '{}/download'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.download(dataset, node, entityids, [product], api_key=api_key)
    }

    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    return response


def download_options(dataset, node, entityids, api_key=None):

    api_key = _get_api_key(api_key)

    url = '{}/downloadoptions'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.download_options(dataset, node, entityids, api_key=api_key)
    }

    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    return response


def get_bulk_download_products():
    raise NotImplementedError


def get_order_products():
    raise NotImplementedError


def hits():
    raise NotImplementedError


def item_basket():
    raise NotImplementedError


def login(username, password, save=True):

    url = '{}/login'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.login(username, password)
    }

    r = requests.post(url, payload)
    if r.status_code is not 200:
        raise USGSError(r.text)

    response = r.json()
    api_key = response["data"]

    if api_key is None:
        raise USGSError(response["error"])

    if save:
        with open(TMPFILE, "w") as f:
            f.write(api_key)

    return response


def logout(api_key=None):

    api_key = _get_api_key(api_key)

    url = '{}/logout'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.logout(api_key)
    }
    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    if os.path.exists(TMPFILE):
        os.remove(TMPFILE)

    return response


def metadata(dataset, node, entityids, extended=False, api_key=None):
    """
    Request metadata for a given scene in a USGS dataset.

    :param dataset:
    :param node:
    :param entityids:
    :param extended:
        Send a second request to the metadata url to get extended metadata on the scene.
    :param api_key:
    """
    api_key = _get_api_key(api_key)

    url = '{}/metadata'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.metadata(dataset, node, entityids, api_key=api_key)
    }
    r = requests.post(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    if extended:
        metadata_urls = map(_get_metadata_url, response['data'])
        results = _async_requests(metadata_urls)
        data = map(lambda idx: _get_extended(response['data'][idx], results[idx]), range(len(response['data'])))

    return response


def remove_bulk_download_scene():
    raise NotImplementedError


def remove_order_scene():
    raise NotImplementedError


def search(dataset, node, lat=None, lng=None, distance=100, ll=None, ur=None, start_date=None, end_date=None,
           where=None, max_results=50000, starting_number=1, sort_order="DESC", extended=False, api_key=None):
    """

    :param dataset:
        USGS dataset (e.g. EO1_HYP_PUB, LANDSAT_8)
    :param node:
        USGS node representing a dataset catalog (e.g. CWIC, EE, HDDS, LPVS)
    :param lat:
        Latitude
    :param lng:
        Longitude
    :param distance:
        Distance in meters used to for a radial search
    :param ll:
        Dictionary of longitude/latitude coordinates for the lower left corner
        of a bounding box search. e.g. { "longitude": 0.0, "latitude": 0.0 }
    :param ur:
        Dictionary of longitude/latitude coordinates for the upper right corner
        of a bounding box search. e.g. { "longitude": 0.0, "latitude": 0.0 }
    :param start_date:
        Start date for when a scene has been acquired
    :param end_date:
        End date for when a scene has been acquired
    :where:
        Dictionary representing key/values for finer grained conditional
        queries. Only a subset of metadata fields are supported. Available
        fields depend on the value of `dataset`, and maybe be found by
        submitting a dataset_fields query.
    :max_results:
        Maximum results returned by the server
    :starting_number:
        Starting offset for results of a query.
    :sort_order:
        Order in which results are sorted. Ascending or descending w.r.t the acquisition date.
    :extended:
        Boolean flag. When true a subsequent query will be sent to the `metadataUrl` returned by
        the first query.
    :api_key:
        API key for EROS. Required for searching.
    """
    api_key = _get_api_key(api_key)

    url = '{}/search'.format(USGS_API)
    payload = {
        "jsonRequest": payloads.search(dataset, node,
        lat=lat, lng=lng,
        distance=100,
        ll=ll, ur=ur,
        start_date=start_date, end_date=end_date,
        where=where,
        max_results=max_results,
        starting_number=starting_number,
        sort_order=sort_order,
        api_key=api_key
    )}
    r = requests.get(url, payload)
    response = r.json()

    _check_for_usgs_error(response)

    if extended:
        metadata_urls = map(_get_metadata_url, response['data']['results'])
        results = _async_requests(metadata_urls)
        data = map(lambda idx: _get_extended(response['data']['results'][idx], results[idx]), range(len(response['data']['results'])))

    return response


def submit_bulk_order():
    raise NotImplementedError


def submit_order():
    raise NotImplementedError


def update_bulk_download_scene():
    raise NotImplementedError


def update_order_scene():
    raise NotImplementedError
