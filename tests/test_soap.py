
import unittest
from usgs import soap

try:
    from django.test.utils import compare_xml
except ImportError:
    compare_xml = None


@unittest.skipIf(compare_xml is None, "Django's test utilities are required.")
class SoapTest(unittest.TestCase):
    
    def test_login(self):
        
        xml1 = soap.login("username", "password")
        xml2 = soap.login("username", "password")
        
        assert compare_xml(xml1, xml2)