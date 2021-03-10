
import json
import pytest
import unittest

from usgs import payloads


def compare_json(s1, s2):
    return json.loads(s1) == json.loads(s2)


class PayloadsTest(unittest.TestCase):

    def test_dataset_filters(self):
        expected = '{"datasetName": "LANDSAT_8_C1"}'
        payload = payloads.dataset_filters("LANDSAT_8_C1")
        assert compare_json(payload, expected)


    def test_download_options(self):
        expected = """{"datasetName": "LANDSAT_8_C1", "entityIds": ["LC80130292014100LGN00", "LC80130282014100LGN00"]}"""
        payload = payloads.download_options("LANDSAT_8_C1", ["LC80130292014100LGN00", "LC80130282014100LGN00"])
        assert compare_json(payload, expected)


    def test_download_request(self):
        expected = """{"downloads": [{"entityId": "LC80130292014100LGN00", "productId": "5e83d0b84df8d8c2"}], "downloadApplication": "EE"}"""
        payload = payloads.download_request("LANDSAT_8_C1", "LC80130292014100LGN00", "5e83d0b84df8d8c2")
        assert compare_json(payload, expected)


    def test_dataset_search(self):

        expected = """{"datasetName": "LANDSAT_8_C1", "catalog": "EE", "temporalFilter": {"start": "2014-10-01T00:00:00Z", "end": "2014-10-01T23:59:59Z"}, "spatialFilter": {"filterType": "mbr", "lowerLeft": {"latitude": 44.60847, "longitude": -99.69639}, "upperRight": {"latitude": 44.60847, "longitude": -99.69639}}}"""

        ll = {"longitude": -99.69639, "latitude": 44.60847}
        ur = {"longitude": -99.69639, "latitude": 44.60847}
        start_date = "2014-10-01T00:00:00Z"
        end_date = "2014-10-01T23:59:59Z"

        payload = payloads.dataset_search(
            "LANDSAT_8_C1", "EE",
            ll=ll, ur=ur,
            start_date=start_date, end_date=end_date)

        assert compare_json(payload, expected)

    
    def test_login(self):
        expected = """{"username": "username", "password": "password"}"""
        payload = payloads.login("username", "password")
        assert compare_json(payload, expected)


    def test_scene_metadata(self):
        expected = """{"datasetName": "LANDSAT_8_C1", "entityId": "LC82260782020217LGN00", "metadataType": "full"}"""
        payload = payloads.scene_metadata("LANDSAT_8_C1", "LC82260782020217LGN00")
        assert compare_json(payload, expected)


    def test_scene_search(self):
        expected = """{"datasetName": "GLS2005", "maxResults": 3, "metadata_type": null, "sceneFilter": {"acquisitionFilter": {"start": "2006-01-01T00:00:00Z", "end": "2007-12-01T00:00:00Z"}, "spatialFilter": {"filterType": "mbr", "lowerLeft": {"longitude": -135, "latitude": 75}, "upperRight": {"longitude": -120, "latitude": 90}}}}"""

        ll = {"longitude": -135, "latitude": 75}
        ur = {"longitude": -120, "latitude": 90}
        start_date = "2006-01-01T00:00:00Z"
        end_date = "2007-12-01T00:00:00Z"

        payload = payloads.scene_search(
            "GLS2005", ll=ll, ur=ur, start_date=start_date,
            end_date=end_date, max_results=3)

        assert compare_json(payload, expected)


    def test_scene_search_radial_distance(self):

        expected = """{"datasetName": "GLS2005", "maxResults": 3, "metadata_type": null, "sceneFilter": {"acquisitionFilter": {"start": "2006-01-01T00:00:00Z", "end": "2007-12-01T00:00:00Z"}, "spatialFilter": {"filterType": "mbr", "lowerLeft": {"longitude": -125.01823502237109, "latitude": 84.99840995696343}, "upperRight": {"longitude": -124.98175340746137, "latitude": 85.00158953883317}}}}"""

        lat = 85
        lng = -125
        dist = 1000
        start_date = "2006-01-01T00:00:00Z"
        end_date = "2007-12-01T00:00:00Z"

        payload = payloads.scene_search(
            "GLS2005", lat=lat, lng=lng, distance=dist, start_date=start_date, end_date=end_date, max_results=3)

        assert compare_json(payload, expected), "wrong result: {r} \n for expected: {e}".format(r=payload, e=expected)