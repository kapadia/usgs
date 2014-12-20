
# Template XML requests required by the USGS Inventory Service
# Requesting data like it's 1999

from xml.etree.ElementTree import Element, SubElement
from usgs import USGSApiKeyRequiredError


def create_root_request():
    root = Element("soapenv:Envelope")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
    root.set("xmlns:soap", "http://earthexplorer.usgs.gov/inventory/soap")

    header = SubElement(root, "soapenv:Header")
    body = SubElement(root, "soapenv:Body")
    
    return (root, body)


def create_api_key_element(parent, api_key):
    api_key_el = SubElement(parent, "apiKey")
    api_key_el.set("xsi:type", "xsd:string")
    api_key_el.text = api_key


def create_node_element(parent, node):
    node_el = SubElement(parent, "node")
    node_el.set("xsi:type", "xsd:string")
    node_el.text = node


def create_dataset_element(parent, dataset):
    dataset_el = SubElement(parent, "datasetName")
    dataset_el.set("xsi:type", "xsd:string")
    dataset_el.text = dataset


def create_clear_bulk_download_order_request(dataset, node, api_key=None):
    """
    This method is used to clear bulk download order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = SubElement(body, "soap:clearBulkDownloadOrder")
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    create_api_key_element(el, api_key)
    create_node_element(el, node)
    create_dataset_element(el, dataset)
    
    return root


def create_clear_order_request(dataset, node, api_key=None):
    """
    This method is used to clear order information from the item basket.
    
    :param dataset:
    
    :param node:
    
    :param api_key:
        API key is required.
    """
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = SubElement(body, "soap:clearOrder")
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    create_api_key_element(el, api_key)
    create_node_element(el, node)
    create_dataset_element(el, dataset)
    
    return root


def create_datasets_request(dataset, node, lower_left=None, upper_right=None, start_date=None, end_date=None, api_key=None):
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
    
    :param lower_left:
        Lower left corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param upper_right:
        Upper right corner of an AOI bounding box - in decimal form
        Longitude/Latitude dictionary
        
        e.g. { "longitude": 0.0, "latitude": 0.0 }
    
    :param start_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param end_date:
        Used for searching scene acquisition - will accept anything
        that the PHP strtotime function can understand
    
    :param node:
        The requested Catalog
    
    :param api_key:
        API key is not required.
        
    """
    
    root, body = create_root_request()
    
    el = SubElement(body, "soap:datasets")
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    create_node_element(el, node)
    create_dataset_element(el, dataset)
    
    if api_key:
        create_api_key_element(el, api_key)
    
    if lower_left and upper_right:
        
        lower_left_el = SubElement(el, "lowerLeft")
        lower_left_el.set("xsi:type", "soap:Service_Class_Coordinate")
        
        ll_lat_el = SubElement(lower_left_el, "latitude")
        ll_lat_el.text = lower_left["latitude"]
        
        ll_lng_el = SubElement(lower_left_el, "longitude")
        ll_lng_el.text = lower_left["longitude"]
        
        upper_right_el = SubElement(el, "upperRight")
        upper_right_el.set("xsi:type", "soap:Service_Class_Coordinate")
        
        ur_lat_el = SubElement(upper_right_el, "latitude")
        ur_lat_el.text = upper_right["latitude"]
        
        ur_lng_el = SubElement(upper_right_el, "longitude")
        ur_lng_el.text = upper_right["longitude"]
        
    if start_date:
        
        start_date_el = SubElement(el, "startDate")
        start_date_el.set("xsi:type", "xsd:string")
        start_date_el.text = start_date
        
    if end_date:
        
        end_date_el = SubElement(el, "endDate")
        end_date_el.set("xsi:type", "xsd:string")
        end_date_el.text = end_date
    
    return root


def create_dataset_fields_request(dataset, node, api_key=None):
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
    
    root, body = create_root_request()
    
    el = SubElement(body, "soap:datasetFields")
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    if api_key:
        create_api_key_element(el, api_key)
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    return root


def create_download_request(dataset, entityIds, products, node, api_key=None):
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
    
    if api_key is None:
        raise USGSApiKeyRequiredError
    
    root, body = create_root_request()
    
    el = SubElement(body, "soap:download")
    el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    create_dataset_element(el, dataset)
    create_node_element(el, node)
    
    entity_ids_el = SubElement(el, "entityIds")
    entity_ids_el.set("xsi:type", "soap:ArrayOfString")
    
    for entityId in entityIds:
        entity_id_el = SubElement(entity_ids_el, "item")
        entity_id_el.set("xsi:type","xsd:string")
        entity_id_el.text = entityId
    
    products_el = SubElement(el, "products")
    products_el.set("xsi:type", "soap:ArrayOfString")
    
    for product in products:
        product_el = SubElement(products_el, "item")
        product_el.set("xsi:type","xsd:string")
        product_el.text = product
        
    return root


def create_download_options_request():
    raise NotImplementedError


def create_get_bulk_download_products_request():
    raise NotImplementedError


def create_get_order_products_request():
    raise NotImplementedError


def create_hits_request():
    raise NotImplementedError


def create_item_basket_request():
    raise NotImplementedError


def create_login_request():
    raise NotImplementedError


def create_logout_request():
    raise NotImplementedError


def create_metadata_request(dataset, node, sceneid):
    root, body = create_root_request()
    
    metadata_el = SubElement(body, "soap:metadata")
    metadata_el.set("soapenv:encodingStyle", "http://schemas.xmlsoap.org/soap/encoding/")
    
    dataset_el = SubElement(metadata_el, "datasetName")
    dataset_el.set("xsi:type", "xsd:string")
    dataset_el.text = dataset
    
    node_el = SubElement(metadata_el, "node")
    node_el.set("xsi:type", "xsd:string")
    node_el.text = node
    
    entity_id_el = SubElement(metadata_el, "entityId")
    entity_id_el.set("xsi:type", "xsd:string")
    entity_id_el.text = sceneid
    
    return root


def create_remove_bulk_download_scene_request():
    raise NotImplementedError


def create_remove_order_scene_request():
    raise NotImplementedError


def create_search_request():
    raise NotImplementedError


def create_submit_bulk_order_request():
    raise NotImplementedError


def create_submit_order_request():
    raise NotImplementedError


def create_update_bulk_download_scene_request():
    raise NotImplementedError


def create_update_order_scene_request():
    raise NotImplementedError


metadata_request = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
   <soapenv:Header/>
   <soapenv:Body>
      <soap:metadata soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <datasetName xsi:type="xsd:string">%(dataset)s</datasetName>
         <node xsi:type="xsd:string">%(node)s</node>
         <entityId xsi:type="xsd:string">%(scene_id)s</entityId>
      </soap:metadata>
   </soapenv:Body>
</soapenv:Envelope>"""

login_request = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
    <soapenv:Header/>
    <soapenv:Body>
      <soap:login soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <username xsi:type="xsd:string">%(username)s</username>
         <raise NotImplementedErrorword xsi:type="xsd:string">%(raise NotImplementedErrorword)s</raise NotImplementedErrorword>
      </soap:login>
    </soapenv:Body>
</soapenv:Envelope>"""

logout_request = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
   <soapenv:Header/>
   <soapenv:Body>
      <soap:logout soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <apiKey xsi:type="xsd:string">%(api_key)s</apiKey>
      </soap:logout>
   </soapenv:Body>
</soapenv:Envelope>"""

download_request = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:download soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <datasetName xsi:type="xsd:string">%(dataset)s</datasetName>
            <node xsi:type="xsd:string">%(node)s</node>
            <apiKey xsi:type="xsd:string">%(api_key)s</apiKey>
            <entityIds xsi:type="soap:ArrayOfString">
            </entityIds>
            <products xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">STANDARD</item>
            </products>
        </soap:download>
    </soapenv:Body>
</soapenv:Envelope>"""

download_options_request = """<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/ XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http:// earthexplorer.usgs.gov/inventory/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:downloadOptions soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <datasetName xsi:type="xsd:string">%(dataset)s</datasetName>
            <apiKey xsi:type="xsd:string">%(api_key)s</apiKey>
            <node xsi:type="xsd:string">%(node)s</node>
            <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">%(scene_id)s</item>
            </entityIds>
        </soap:downloadOptions>
    </soapenv:Body>
</soapenv:Envelope>"""

search_request = """<?xml version="1.0"?>
<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
    <soapenv:Header/>
    <soapenv:Body>
        <soap:search soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <apiKey xsi:type="xsd:string">%(api_key)s</apiKey>
            <datasetName xsi:type="xsd:string">%(dataset)s</datasetName>
            <maxResults xsi:type="xsd:int">50000</maxResults>
            <startingNumber xsi:type="xsd:int">1</startingNumber>
            <sortOrder xsi:type="xsd:string">ASC</sortOrder>
            <node xsi:type="xsd:string">%(node)s</node>
        </soap:search>
    </soapenv:Body>
</soapenv:Envelope>"""

lower_left_search = """<lowerLeft xsi:type="soap:Service_Class_Coordinate">
    <latitude xsi:type="xsd:double">%(lat_ll).6f</latitude>
    <longitude xsi:type="xsd:double">%(lng_ll).6f</longitude>
</lowerLeft>"""
upper_right_search = """<upperRight xsi:type="soap:Service_Class_Coordinate">
    <latitude xsi:type="xsd:double">%(lat_ur).6f</latitude>
    <longitude xsi:type="xsd:double">%(lng_ur).6f</longitude>
</upperRight>"""

start_date_search = """<startDate xsi:type="xsd:string">%(start_date)s</startDate>"""
end_date_search = """<endDate xsi:type="xsd:string">%(end_date)s</endDate>"""