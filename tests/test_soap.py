import re
import pytest
import unittest
from usgs import soap
from xml.dom import minidom


def strip_quotes(want, got):
    """
    Strip quotes of doctests output values:
    >>> strip_quotes("'foo'")
    "foo"
    >>> strip_quotes('"foo"')
    "foo"
    """
    def is_quoted_string(s):
        s = s.strip()
        return (len(s) >= 2
                and s[0] == s[-1]
                and s[0] in ('"', "'"))

    def is_quoted_unicode(s):
        s = s.strip()
        return (len(s) >= 3
                and s[0] == 'u'
                and s[1] == s[-1]
                and s[1] in ('"', "'"))

    if is_quoted_string(want) and is_quoted_string(got):
        want = want.strip()[1:-1]
        got = got.strip()[1:-1]
    elif is_quoted_unicode(want) and is_quoted_unicode(got):
        want = want.strip()[2:-1]
        got = got.strip()[2:-1]
    return want, got


def compare_xml(want, got):
    """Tries to do a 'xml-comparison' of want and got.  Plain string
    comparison doesn't always work because, for example, attribute
    ordering should not be important. Comment nodes are not considered in the
    comparison. Leading and trailing whitespace is ignored on both chunks.
    Based on http://codespeak.net/svn/lxml/trunk/src/lxml/doctestcompare.py
    """
    _norm_whitespace_re = re.compile(r'[ \t\n][ \t\n]+')

    def norm_whitespace(v):
        return _norm_whitespace_re.sub(' ', v)

    def child_text(element):
        return ''.join(c.data for c in element.childNodes
                       if c.nodeType == minidom.Node.TEXT_NODE)

    def children(element):
        return [c for c in element.childNodes
                if c.nodeType == minidom.Node.ELEMENT_NODE]

    def norm_child_text(element):
        return norm_whitespace(child_text(element))

    def attrs_dict(element):
        return dict(element.attributes.items())

    def check_element(want_element, got_element):
        if want_element.tagName != got_element.tagName:
            return False
        if norm_child_text(want_element) != norm_child_text(got_element):
            return False
        if attrs_dict(want_element) != attrs_dict(got_element):
            return False
        want_children = children(want_element)
        got_children = children(got_element)
        if len(want_children) != len(got_children):
            return False
        for want, got in zip(want_children, got_children):
            if not check_element(want, got):
                return False
        return True

    def first_node(document):
        for node in document.childNodes:
            if node.nodeType != minidom.Node.COMMENT_NODE:
                return node

    want, got = strip_quotes(want, got)
    want = want.strip().replace('\\n', '\n')
    got = got.strip().replace('\\n', '\n')

    # If the string is not a complete xml document, we may need to add a
    # root element. This allow us to compare fragments, like "<foo/><bar/>"
    if not want.startswith('<?xml'):
        wrapper = '<root>%s</root>'
        want = wrapper % want
        got = wrapper % got

    # Parse the want and got strings, and compare the parsings.
    want_root = first_node(minidom.parseString(want))
    got_root = first_node(minidom.parseString(got))

    return check_element(want_root, got_root)


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

        ll = {"longitude": -99.69639, "latitude": 44.60847}
        ur = {"longitude": -99.69639, "latitude": 44.60847}
        start_date = "2014-10-01T00:00:00Z"
        end_date = "2014-10-01T23:59:59Z"

        request = soap.datasets("L8", "EE", ll=ll, ur=ur, start_date=start_date, end_date=end_date,
                                api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

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
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:download soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
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

        request = soap.download("LANDSAT_8", "EE", ["LC80130292014100LGN00"], ["STANDARD"], api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_download_options(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:downloadOptions soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:downloadOptions>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        request = soap.download_options("LANDSAT_8", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_get_bulk_download_products(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:getBulkDownloadProducts soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:getBulkDownloadProducts>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        request = soap.get_bulk_download_products("LANDSAT_8", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_get_order_products(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:getOrderProducts soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:getOrderProducts>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        request = soap.get_order_products("LANDSAT_8", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_item_basket(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:itemBasket soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:itemBasket>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        request = soap.item_basket(api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

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

        request = soap.logout(api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_metadata(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:metadata soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">LANDSAT_8</datasetName>
              <node xsi:type="xsd:string">EE</node>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <entityIds xsi:type="soap:ArrayOfString">
                <item xsi:type="xsd:string">LC80130292014100LGN00</item>
                <item xsi:type="xsd:string">LC80130282014100LGN00</item>
              </entityIds>
            </soap:metadata>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        request = soap.metadata("LANDSAT_8", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

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
        pytest.skip("Not yet implemented")

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
        pytest.skip("Not yet implemented")

    def test_search(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:search soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <datasetName xsi:type="xsd:string">GLS2005</datasetName>
              <node xsi:type="xsd:string">EE</node>
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
              <maxResults xsi:type="xsd:int">3</maxResults>
              <startingNumber xsi:type="xsd:int">1</startingNumber>
              <sortOrder xsi:type="xsd:string">ASC</sortOrder>
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
            </soap:search>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        ll = {"longitude": -135, "latitude": 75}
        ur = {"longitude": -120, "latitude": 90}
        start_date = "2006-01-01T00:00:00Z"
        end_date = "2007-12-01T00:00:00Z"

        request = soap.search("GLS2005", "EE", ll=ll, ur=ur, start_date=start_date, end_date=end_date, max_results=3,
                              sort_order="ASC", api_key="USERS API KEY")
        request = minidom.parseString(request).toprettyxml()

        assert compare_xml(request, expected)

    def test_submit_bulk_order(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:submitBulkDownloadOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
            </soap:submitBulkDownloadOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        pytest.skip("Not yet implemented")

    def test_submit_order(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
          <soapenv:Header/>
          <soapenv:Body>
            <soap:submitOrder soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
              <apiKey xsi:type="xsd:string">USERS API KEY</apiKey>
              <node xsi:type="xsd:string">EE</node>
            </soap:submitOrder>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        pytest.skip("Not yet implemented")

    def test_update_bulk_download_scene(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
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
        pytest.skip("Not yet implemented")

    def test_update_order_scene(self):

        expected = """
        <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://earthexplorer.usgs.gov/inventory/soap">
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
        pytest.skip("Not yet implemented")
