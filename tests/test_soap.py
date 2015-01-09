
import pytest
import unittest
from usgs import soap
from xml.dom import minidom

try:
    from django.test.utils import compare_xml
except ImportError:
    compare_xml = None


@unittest.skipIf(compare_xml is None, "Django's test utilities are required.")
class SoapTest(unittest.TestCase):


    def test_clear_bulk_download_order(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
              <soap:clearBulkDownloadOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <node xsi:type="xsd:string">EE</node>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:clearBulkDownloadOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
        request = soap.clear_bulk_download_order("LANDSAT_8", "EE", api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()
        
        assert compare_xml(request, expected)
        
        
    def test_clear_order(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
              <soap:clearOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <node xsi:type="xsd:string">EE</node>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:clearOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
        request = soap.clear_order("LANDSAT_8", "EE", api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()
        
        assert compare_xml(request, expected)
        
    
    def test_datasets(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:datasets soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <node xsi:type="xsd:string">EE</node>
              <datasetName xsi:type="xsd:string">L8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <lowerLeft xsi:type="soap:Service_Class_Coordinate">
                <latitude xsi:type="xsd:double">44.60847</latitude>
                <longitude xsi:type="xsd:double">-99.69639</longitude>
              </lowerLeft>
              <upperRight xsi:type="soap:Service_Class_Coordinate">
                <latitude xsi:type="xsd:double">44.60847</latitude>
                <longitude xsi:type="xsd:double">-99.69639</longitude>
              </upperRight>
              <startDate xsi:type="xsd:string">2014-10-01T00:00:00Z</startDate>
              <endDate xsi:type="xsd:string">2014-10-01T23:59:59Z</endDate>
            </soap:datasets>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
        ll = { "longitude": -99.69639, "latitude": 44.60847 }
        ur = { "longitude": -99.69639, "latitude": 44.60847 }
        start_date = "2014-10-01T00:00:00Z"
        end_date = "2014-10-01T23:59:59Z"
        
        request = soap.datasets("L8", "EE", ll=ll, ur=ur, start_date=start_date, end_date=end_date, api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()
        
        print request
        
        assert compare_xml(request, expected)
        
    
    def test_dataset_fields(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:datasetFields soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:datasetFields>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
        request = soap.dataset_fields("LANDSAT_8", "EE", api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()
        
        assert compare_xml(request, expected)
    
       
    def test_download(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:download soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
              </entityIds>
              <products xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">STANDARD</item>
              </products>
            </soap:download>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    def test_download_options(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:downloadOptions soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:downloadOptions>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
    
    def test_get_bulk_download_products(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:getBulkDownloadProducts soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:getBulkDownloadProducts>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    def test_get_order_products(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:getOrderProducts soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:getOrderProducts>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_item_basket(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:itemBasket soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:itemBasket>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_login(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:login soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <username xsi:type="xsd:string">username</username>
              <password xsi:type="xsd:string">password</password>
            </soap:login>
            </soapenv:Body>
        </soapenv:Envelope>
        """
        
        request = soap.login("username", "password")
        request = minidom.parseString(request).toprettyxml()
        
        assert compare_xml(request, expected)
    
    
    def test_logout(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:logout soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:logout>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_metadata(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:metadata soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:metadata>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        
        
    
    def test_remove_bulk_download_scene(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:removeBulkDownloadScene soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:removeBulkDownloadScene>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_remove_order_scene(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:removeOrderScene soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:removeOrderScene>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_search(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:search soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">GLS2005</datasetName>
              <lowerLeft xsi:type="soap:Service_Class_Coordinate">
                <latitude xsi:type="xsd:double">75</latitude>
                <longitude xsi:type="xsd:double">-135</longitude>
              </lowerLeft>
              <upperRight xsi:type="soap:Service_Class_Coordinate">
                <latitude xsi:type="xsd:double">90</latitude>
                <longitude xsi:type="xsd:double">-120</longitude>
              </upperRight>
              <startDate xsi:type="xsd:string">2006-01-01T00:00:00Z</startDate>
              <endDate xsi:type="xsd:string">2007-12-01T00:00:00Z</endDate>
              <node xsi:type="xsd:string">EE</node>
              <maxResults xsi:type="xsd:int">3</maxResults>
              <startingNumber xsi:type="xsd:int">1</startingNumber>
              <sortOrder xsi:type="xsd:string">ASC</sortOrder>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:search>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_submit_bulk_order(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:submitBulkDownloadOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
            </soap:submitBulkDownloadOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_submit_order(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:submitOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
            </soap:submitOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_update_bulk_download_scene(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:updateBulkDownloadScene soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <orderingId xsi:type="xsd:string">LC80130292014100LGN00</orderingId>
              <downloadCodes xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">STANDARD</item>
              </downloadCodes>
            </soap:updateBulkDownloadScene>
          </soapenv:Body>
        </soapenv:Envelope>
        """
    
    
    
    def test_update_order_scene(self):
        
        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="https://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:updateOrderScene soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
              <datasetName xsi:type="xsd:string">LANDSAT_TM</datasetName>
              <orderingId xsi:type="xsd:string">LT50980761990085ASA00</orderingId>
              <productCode xsi:type="xsd:string">T273</productCode>
              <option xsi:type="xsd:string">None</option>
              <outputMedia xsi:type="xsd:string">DWNLD</outputMedia>
            </soap:updateOrderScene>
          </soapenv:Body>
        </soapenv:Envelope>
        """