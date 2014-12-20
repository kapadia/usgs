
# Template XML requests required by the USGS Inventory Service
# Requesting data like it's 1999

from xml.etree.ElementTree import Element, SubElement


def create_root_request():
    root = Element("soapenv:Envelope")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    root.set("xmlns:soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
    root.set("xmlns:soap", "http://earthexplorer.usgs.gov/inventory/soap")

    header = SubElement(root, "soapenv:Header")
    body = SubElement(root, "soapenv:Body")
    return (root, body)


def create_clear_bulk_download_order_request():
    raise NotImplementedError


def create_clear_order_request():
    raise NotImplementedError


def create_datasets_request():
    raise NotImplementedError


def create_dataset_fields_request():
    raise NotImplementedError


def create_download_request():
    raise NotImplementedError


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