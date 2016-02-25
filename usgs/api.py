
import os
from os.path import expanduser
from xml.etree import ElementTree
import requests
from requests_futures.sessions import FuturesSession

from usgs import USGS_API, USGSError
from usgs import soap, xsi


TMPFILE = os.path.join(expanduser("~"), ".usgs")
NAMESPACES = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "ns1": "https://earthexplorer.usgs.gov/inventory/soap",
    "eemetadata": "http://earthexplorer.usgs.gov/eemetadata.xsd"
}


def _get_api_key():

    api_key = None

    if os.path.exists(TMPFILE):
        with open(TMPFILE, "r") as f:
            api_key = f.read()

    return api_key


def _check_for_usgs_error(root):

    fault_code_el = root.find("SOAP-ENV:Body/SOAP-ENV:Fault/faultcode", NAMESPACES)

    if fault_code_el is None:
        return

    fault_string_el = root.find("SOAP-ENV:Body/SOAP-ENV:Fault/faultstring", NAMESPACES)

    fault_code = fault_code_el.text
    fault_string = fault_string_el.text

    raise USGSError('%s: %s' % (fault_code, fault_string))


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
    futures = [session.get(url) for url in urls]
    return [future.result() for future in futures]


def _get_metadata_url(scene):
    return scene.get('metadataUrl')


def clear_bulk_download_order():
    raise NotImplementedError


def clear_order():
    raise NotImplementedError


def datasets(dataset, node, ll=None, ur=None, start_date=None, end_date=None):

    api_key = _get_api_key()

    xml = soap.datasets(dataset, node, ll=ll, ur=ur, start_date=start_date, end_date=end_date, api_key=api_key)
    r = requests.post(USGS_API, xml)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:datasetsResponse/return/item", NAMESPACES)

    data = map(lambda item: {el.tag: xsi.get(el) for el in item}, items)

    return data


def dataset_fields(dataset, node):

    api_key = _get_api_key()

    xml = soap.dataset_fields(dataset, node, api_key=api_key)
    r = requests.post(USGS_API, xml)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:datasetFieldsResponse/return/item", NAMESPACES)
    data = map(lambda item: {el.tag: xsi.get(el) for el in item}, items)

    return data


def download(dataset, node, entityids, product='STANDARD', api_key=None):
    """
    Though USGS supports multiple products in a single request, there's
    ambiguity in the returned list. This wrapper only allows a single
    product per request.

    Additionally, the response has no indiction which URL is associated
    with which scene/entity id. The URL can be parsed, but the structure
    varies depending on the product.
    """

    api_key = api_key if api_key else _get_api_key()

    xml = soap.download(dataset, node, entityids, [product], api_key=api_key)
    r = requests.post(USGS_API, xml)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:downloadResponse/return/item", NAMESPACES)

    data = map(lambda el: xsi.get(el), items)

    return data


def download_options(dataset, node, entityids):

    api_key = _get_api_key()

    xml = soap.download_options(dataset, node, entityids, api_key=api_key)
    r = requests.post(USGS_API, xml)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:downloadOptionsResponse/return/item/downloadOptions/item", NAMESPACES)

    data = map(lambda item: {el.tag: xsi.get(el) for el in item}, items)

    return data


def get_bulk_download_products():
    raise NotImplementedError


def get_order_products():
    raise NotImplementedError


def hits():
    raise NotImplementedError


def item_basket():
    raise NotImplementedError


def login(username, password, save=True):
    xml = soap.login(username, password)
    r = requests.post(USGS_API, xml)

    if r.status_code is not 200:
        raise USGSError(r.text)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    element = root.find("SOAP-ENV:Body/ns1:loginResponse/return", NAMESPACES)

    api_key = element.text

    if save:
        with open(TMPFILE, "w") as f:
            f.write(api_key)

    return api_key


def logout():

    api_key = _get_api_key()

    xml = soap.logout(api_key=api_key)
    requests.post(USGS_API, xml)

    if os.path.exists(TMPFILE):
        os.remove(TMPFILE)

    return True


def metadata(dataset, node, sceneids, extended=False, api_key=None):
    """
    Request metadata for a given scene in a USGS dataset.

    :param dataset:
    :param node:
    :param sceneids:
    :param extended:
        Send a second request to the metadata url to get extended metadata on the scene.
    :param api_key:
    """
    api_key = api_key if api_key else _get_api_key()

    xml = soap.metadata(dataset, node, sceneids, api_key=api_key)
    r = requests.post(USGS_API, xml)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:metadataResponse/return/item", NAMESPACES)

    data = map(lambda item: {el.tag: xsi.get(el) for el in item}, items)

    if extended:
        metadata_urls = map(_get_metadata_url, data)
        results = _async_requests(metadata_urls)
        data = map(lambda idx: _get_extended(data[idx], results[idx]), range(len(data)))

    return data


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
        API key for EROS. Not required for searching.

    .. todo:: Export metadata from the search results e.g.

        <numberReturned xsi:type="xsd:int">41</numberReturned>
        <totalHits xsi:type="xsd:int">41</totalHits>
        <firstRecord xsi:type="xsd:int">1</firstRecord>
        <lastRecord xsi:type="xsd:int">41</lastRecord>
        <nextRecord xsi:type="xsd:int">41</nextRecord>
    """
    api_key = api_key if api_key else _get_api_key()

    xml = soap.search(dataset, node, lat=lat, lng=lng, distance=100, ll=ll, ur=ur, start_date=start_date,
                      end_date=end_date, where=where, max_results=max_results, starting_number=starting_number,
                      sort_order=sort_order, api_key=api_key)
    r = requests.post(USGS_API, xml)

    # Find out what's going on with usgs servers!
    try:
        r.raise_for_status()
    except:
        print(r.text)

    root = ElementTree.fromstring(r.text)
    _check_for_usgs_error(root)

    items = root.findall("SOAP-ENV:Body/ns1:searchResponse/return/results/item", NAMESPACES)

    data = map(lambda item: {el.tag: xsi.get(el) for el in item}, items)

    if extended:
        metadata_urls = map(_get_metadata_url, data)
        results = _async_requests(metadata_urls)
        data = map(lambda idx: _get_extended(data[idx], results[idx]), range(len(data)))

    return data


def submit_bulk_order():
    raise NotImplementedError


def submit_order():
    raise NotImplementedError


def update_bulk_download_scene():
    raise NotImplementedError


def update_order_scene():
    raise NotImplementedError
