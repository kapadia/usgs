
import json
import pytest
import unittest

from usgs import payloads


def compare_json(s1, s2):
    return json.loads(s1) == json.loads(s2)


class PayloadsTest(unittest.TestCase):


    def test_clear_bulk_download_order(self):
        pytest.skip("Not implemented")


    def test_clear_order(self):
        pytest.skip("Not implemented")


    def test_dataset_fields(self):

        expected = '{"node": "EE", "datasetName": "LANDSAT_8_C1", "apiKey": "USERS API KEY"}'
        payload = payloads.dataset_fields("LANDSAT_8_C1", "EE", api_key="USERS API KEY")

        assert compare_json(payload, expected)


    def test_datasets(self):

        expected = """{"node": "EE", "startDate": "2014-10-01T00:00:00Z", "datasetName": "LANDSAT_8_C1", "apiKey": "USERS API KEY", "endDate": "2014-10-01T23:59:59Z", "upperRight": {"latitude": 44.60847, "longitude": -99.69639}, "lowerLeft": {"latitude": 44.60847, "longitude": -99.69639}}"""

        ll = {"longitude": -99.69639, "latitude": 44.60847}
        ur = {"longitude": -99.69639, "latitude": 44.60847}
        start_date = "2014-10-01T00:00:00Z"
        end_date = "2014-10-01T23:59:59Z"

        payload = payloads.datasets(
            "LANDSAT_8_C1", "EE",
            ll=ll, ur=ur,
            start_date=start_date, end_date=end_date,
            api_key="USERS API KEY"
        )

        assert compare_json(payload, expected)


    def test_download(self):

        expected = """{"node": "EE", "products": ["STANDARD"], "datasetName": "LANDSAT_8_C1", "apiKey": "USERS API KEY", "entityIds": ["LC80130292014100LGN00"]}"""

        payload = payloads.download("LANDSAT_8_C1", "EE", ["LC80130292014100LGN00"], ["STANDARD"], api_key="USERS API KEY")
        assert compare_json(payload, expected)


    def test_download_options(self):

        expected = """{"node": "EE", "datasetName": "LANDSAT_8_C1", "apiKey": "USERS API KEY", "entityIds": ["LC80130292014100LGN00", "LC80130282014100LGN00"]}"""

        payload = payloads.download_options("LANDSAT_8_C1", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        assert compare_json(payload, expected)


    def test_get_bulk_download_products(self):
        pytest.skip("Not implemented")


    def test_get_order_products(self):
        pytest.skip("Not implemented")


    def test_item_basket(self):
        pytest.skip("Not implemented")


    def test_login(self):

        expected = """{"username": "username", "password": "password", "authType": "", "catalogId": "EE"}"""

        payload = payloads.login("username", "password")
        assert compare_json(payload, expected)


    def test_logout(self):

        expected = """{"apiKey": "USERS API KEY"}"""

        payload = payloads.logout(api_key="USERS API KEY")
        assert compare_json(payload, expected)


    def test_metadata(self):

        expected = """{"node": "EE", "datasetName": "LANDSAT_8_C1", "apiKey": "USERS API KEY", "entityIds": ["LC80130292014100LGN00", "LC80130282014100LGN00"]}"""

        payload = payloads.metadata("LANDSAT_8_C1", "EE", ["LC80130292014100LGN00", "LC80130282014100LGN00"], api_key="USERS API KEY")
        assert compare_json(payload, expected)


    def test_remove_bulk_download_scene(self):
        pytest.skip("Not implemented")


    def test_remove_order_scene(self):
        pytest.skip("Not implemented")


    def test_search(self):

        expected = """{"node": "EE", "datasetName": "GLS2005", "apiKey": "USERS API KEY", "upperRight": {"latitude": 90, "longitude": -120}, "maxResults": 3, "startingNumber": 1, "sortOrder": "ASC", "lowerLeft": {"latitude": 75, "longitude": -135}, "temporalFilter": {"dateField": "search_date", "endDate": "2007-12-01T00:00:00Z", "startDate": "2006-01-01T00:00:00Z"}}"""

        ll = {"longitude": -135, "latitude": 75}
        ur = {"longitude": -120, "latitude": 90}
        start_date = "2006-01-01T00:00:00Z"
        end_date = "2007-12-01T00:00:00Z"

        payload = payloads.search("GLS2005", "EE", ll=ll, ur=ur, start_date=start_date, end_date=end_date, max_results=3,
                              sort_order="ASC", api_key="USERS API KEY")
        assert compare_json(payload, expected)


    def test_submit_bulk_order(self):
        pytest.skip("Not implemented")


    def test_submit_order(self):
        pytest.skip("Not implemented")


    def test_update_bulk_download_scene(self):
        pytest.skip("Not implemented")


    def test_update_order_scene(self):
        pytest.skip("Not implemented")
