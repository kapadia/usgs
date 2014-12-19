
# Template XML requests required by the USGS Inventory Service
# Requesting data like it's 1999

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
         <password xsi:type="xsd:string">%(password)s</password>
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