
import os
from xml.etree import ElementTree
import requests

from usgs import USGS_API, USGSConnectionError
from usgs import soap

TMPFILE = os.path.join("/", "tmp", "usgs")
NAMESPACES = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "ns1": "https://earthexplorer.usgs.gov/inventory/soap"
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
    

def datasets(dataset, node, lower_left=None, upper_right=None, start_date=None, end_date=None):
    
    api_key = _get_api_key()
    
    xml = soap.datasets(dataset, node, lower_left=lower_left, upper_right=upper_right, start_date=start_date, end_date=end_date, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    return r.text
    

def dataset_fields(dataset, node):
    
    api_key = _get_api_key()
    
    xml = soap.dataset_fields(dataset, node, api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    return r.text
    

def download():
    raise NotImplementedError
    

def download_options():
    raise NotImplementedError
    

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
    
    body = root.find("SOAP-ENV:Body", NAMESPACES)
    login_response = body.find("ns1:loginResponse", NAMESPACES)
    api_key = login_response.find("return").text
    
    with open(TMPFILE, "w") as f:
        f.write(api_key)
    
    return api_key
    
    
def logout():
    
    api_key = _get_api_key()
    
    xml = soap.logout(api_key=api_key)
    r = requests.post(USGS_API, xml)
    
    if os.path.exists(TMPFILE):
        os.remove(TMPFILE)
    
    return r.text
    

def metadata():
    raise NotImplementedError
    

def remove_bulk_download_scene():
    raise NotImplementedError
    

def remove_order_scene():
    raise NotImplementedError
    

def search():
    raise NotImplementedError
    

def submit_bulk_order():
    raise NotImplementedError
    

def submit_order():
    raise NotImplementedError
    

def update_bulk_download_scene():
    raise NotImplementedError
    

def update_order_scene():
    raise NotImplementedError
    