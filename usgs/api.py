
import os
from xml.etree import ElementTree
import requests

from usgs import USGS_API, USGSConnectionError
from usgs import soap, xsi


TMPFILE = os.path.join("/", "tmp", "usgs")
NAMESPACES = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "ns1": "https://earthexplorer.usgs.gov/inventory/soap",
}

def _get_api_key():
    
    api_key = None
    
    if os.path.exists(TMPFILE):
        with open(TMPFILE, "r") as f:
            api_key = f.read()
    
    return api_key


def clear_bulk_download_order():
    raise NotImplementedError

    
def clear_order():
    raise NotImplementedError
    

def datasets(dataset, node, ll=None, ur=None, start_date=None, end_date=None):
    
    api_key = _get_api_key()
    
    xml = soap.datasets(dataset, node, ll=ll, ur=ur, start_date=start_date, end_date=end_date, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    root = ElementTree.fromstring(r.text)
    items = root.findall("SOAP-ENV:Body/ns1:datasetsResponse/return/item", NAMESPACES)
    
    data = map(lambda item: { el.tag: xsi.get(el) for el in item }, items)
    
    return data


def dataset_fields(dataset, node):
    
    api_key = _get_api_key()
    
    xml = soap.dataset_fields(dataset, node, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    root = ElementTree.fromstring(r.text)
    items = root.findall("SOAP-ENV:Body/ns1:datasetFieldsResponse/return/item", NAMESPACES)
    data = map(lambda item: { el.tag: xsi.get(el) for el in item }, items)
    
    return data
    

def download(dataset, node, entityids, products):
    raise NotImplementedError
    # api_key = _get_api_key()
    #
    # download(dataset, node, entityids, products, api_key=None):
    # xml = soap.download()
    

def download_options(dataset, node, entityids):
    
    api_key = _get_api_key()
    
    xml = soap.download_options(dataset, node, entityids, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    root = ElementTree.fromstring(r.text)
    items = root.findall("SOAP-ENV:Body/ns1:downloadOptionsResponse/return/item/downloadOptions/item", NAMESPACES)
    print items
    
    data = map(lambda item: { el.tag: xsi.get(el) for el in item }, items)
    
    return data


def get_bulk_download_products():
    raise NotImplementedError
    

def get_order_products():
    raise NotImplementedError
    

def hits():
    raise NotImplementedError
    

def item_basket():
    raise NotImplementedError
    
    
def login(username, password):
    
    xml = soap.login(username, password)
    r = requests.post(USGS_API, xml)
    
    if r.status_code != 200:
        raise USGSConnectionError
    
    root = ElementTree.fromstring(r.text)
    element = root.find("SOAP-ENV:Body/ns1:loginResponse/return", NAMESPACES)
    
    api_key = element.text
    
    with open(TMPFILE, "w") as f:
        f.write(api_key)
    
    return api_key
    
    
def logout():
    
    api_key = _get_api_key()
    
    xml = soap.logout(api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    if os.path.exists(TMPFILE):
        os.remove(TMPFILE)
    
    return True
    

def metadata(dataset, node, sceneids, api_key=None):
    
    api_key = _get_api_key()
    
    xml = soap.metadata(dataset, node, sceneids, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    if r.status_code != 200:
        raise USGSConnectionError
    
    root = ElementTree.fromstring(r.text)
    items = root.findall("SOAP-ENV:Body/ns1:metadataResponse/return/item", NAMESPACES)
    
    data = map(lambda item: { el.tag: xsi.get(el) for el in item }, items)
    
    return data
    

def remove_bulk_download_scene():
    raise NotImplementedError
    

def remove_order_scene():
    raise NotImplementedError
    

def search(dataset, node, lat=None, lng=None, distance=100, ll=None, ur=None, start_date=None, end_date=None, max_results=50000, starting_number=1, sort_order="DESC", api_key=None):
    """
    .. todo:: Export metadata from the search results e.g.
    
        <numberReturned xsi:type="xsd:int">41</numberReturned>
        <totalHits xsi:type="xsd:int">41</totalHits>
        <firstRecord xsi:type="xsd:int">1</firstRecord>
        <lastRecord xsi:type="xsd:int">41</lastRecord>
        <nextRecord xsi:type="xsd:int">41</nextRecord>
    """
    api_key = _get_api_key()
    
    xml = soap.search(dataset, node, lat=lat, lng=lng, distance=100, ll=ll, ur=ur, start_date=start_date, end_date=end_date, max_results=max_results, starting_number=starting_number, sort_order=sort_order, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    if r.status_code != 200:
        raise USGSConnectionError
    
    root = ElementTree.fromstring(r.text)
    items = root.findall("SOAP-ENV:Body/ns1:searchResponse/return/results/item", NAMESPACES)
    
    data = map(lambda item: { el.tag: xsi.get(el) for el in item }, items)
    
    return data


def submit_bulk_order():
    raise NotImplementedError
    

def submit_order():
    raise NotImplementedError
    

def update_bulk_download_scene():
    raise NotImplementedError
    

def update_order_scene():
    raise NotImplementedError
    