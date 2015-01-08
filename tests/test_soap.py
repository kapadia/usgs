
import unittest
from usgs import soap
from xml.dom import minidom

try:
    from django.test.utils import compare_xml
except ImportError:
    compare_xml = None


@unittest.skipIf(compare_xml is None, "Django's test utilities are required.")
class SoapTest(unittest.TestCase):
    
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