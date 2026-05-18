import unittest
from unittest import mock

import requests

from usgs import api, USGSError
from .MockPost import MockPost


def check_root_keys(response):

    expected_keys = ["requestId", "version", "sessionId", "data", "errorCode", "errorMessage"]
    for key in expected_keys:
        if key not in response:
            return False

    return True

@mock.patch('usgs.api.requests.Session.post', MockPost('dataset-fields.json'))
def test_dataset_filters():

    expected_keys = ["id", "legacyFieldId", "dictionaryLink", "fieldConfig", "fieldLabel", "searchSql"]
    response = api.dataset_filters("LANDSAT_8_C1")

    assert check_root_keys(response)

    for item in response['data']:
        for key in expected_keys:
            assert key in item

@mock.patch('usgs.api.requests.Session.post', MockPost('download-options.json'))
def test_download_options():

    expected_keys = ["id", "displayId", "entityId", "datasetId", "available", "filesize", "productName", "productCode", "bulkAvailable", "downloadSystem", "secondaryDownloads"]
    response = api.download_options("LANDSAT_8_C1", ["LC82260782020217LGN00"])

    assert check_root_keys(response)

    for item in response["data"]:
        for key in expected_keys:
            assert key in item

@mock.patch('usgs.api.requests.Session.post', MockPost('dataset-download-options.json'))
def test_dataset_download_options():
    expected_keys = ['productId', 'productCode', 'productName']
    response = api.dataset_download_options("LANDSAT_8_C1")

    assert check_root_keys(response)

    for item in response["data"]:
        for key in expected_keys:
            assert key in item

@mock.patch('usgs.api.requests.Session.post', MockPost('download-request.json'))
def test_download_request():

    expected_keys = ['availableDownloads', 'duplicateProducts', 'preparingDownloads', 'failed', 'newRecords', 'numInvalidScenes']
    response = api.download_request("LANDSAT_8_C1", "LC82260782020217LGN00", "5e83d0b84df8d8c2")

    assert check_root_keys

    for key in response["data"]:
        assert key in expected_keys

@mock.patch('usgs.api.requests.Session.post', MockPost('dataset-search.json'))
def test_dataset_search():

    expected_keys = [
        'abstractText', 'acquisitionStart', 'acquisitionEnd', 'catalogs', 'collectionName',
        'collectionLongName', 'datasetId', 'datasetAlias', 'datasetCategoryName',
        'dataOwner', 'dateUpdated', 'doiNumber', 'ingestFrequency', 'keywords',
        'legacyId', 'sceneCount', 'spatialBounds', 'temporalCoverage',
        'supportCloudCover', 'supportDeletionSearch']
    response = api.dataset_search()

    assert check_root_keys(response)
    assert len(response['data']) == 1163
    for key in expected_keys:
        assert key in response['data'][0]

@mock.patch('usgs.api.requests.Session.post', MockPost('scene-metadata.json'))
def test_scene_metadata():

    expected_keys = [
        'browse', 'cloudCover', 'entityId', 'displayId', 'orderingId', 'metadata',
        'hasCustomizedMetadata', 'options', 'selected', 'spatialBounds', 'spatialCoverage',
        'temporalCoverage', 'publishDate']

    response = api.scene_metadata(
        "LANDSAT_8_C1", "LC82260782020217LGN00")
    assert check_root_keys(response)

    for key in expected_keys:
        assert key in response['data']

@mock.patch('usgs.api.requests.Session.post', MockPost('scene-search.json'))
def test_scene_search():
    expected_keys = [
        'browse', 'cloudCover', 'entityId', 'displayId', 'orderingId', 'metadata',
        'hasCustomizedMetadata', 'options', 'selected', 'spatialBounds', 'spatialCoverage',
        'temporalCoverage', 'publishDate']

    where = {
        "filter_id": "5e83d0b8fb079b8b",
        "value": "T1"
    }
    response = api.scene_search(
        "LANDSAT_8_C1", start_date='2016-09-11', end_date='2016-09-12', metadata_type="summary",
        max_results=1, lat=-33.463623929871886, lng=-70.54248332977295, where=where)

    assert check_root_keys(response)
    assert len(response['data']["results"]) == 1

    for expected_key in expected_keys:
        assert expected_key in response['data']["results"][0]


class HttpErrorTests(unittest.TestCase):

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_dataset_filters_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.dataset_filters("LANDSAT_8_C1")
        assert "HTTP error occurred during dataset filters request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_download_options_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.download_options("LANDSAT_8_C1", ["LC82260782020217LGN00"])
        assert "HTTP error occurred during download options request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_dataset_download_options_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.dataset_download_options("LANDSAT_8_C1")
        assert "HTTP error occurred during dataset download options request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_download_request_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.download_request(
                "LANDSAT_8_C1", "LC82260782020217LGN00", "5e83d0b84df8d8c2")
        assert "HTTP error occurred during download request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_dataset_search_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.dataset_search()
        assert "HTTP error occurred during dataset search request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_login_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.login("user", "token", save=False)
        assert "HTTP error occurred during login request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_scene_metadata_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.scene_metadata("LANDSAT_8_C1", "LC82260782020217LGN00")
        assert "HTTP error occurred during scene metadata request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    def test_scene_search_http_error(self):
        with self.assertRaises(USGSError) as cm:
            api.scene_search("LANDSAT_8_C1")
        assert "HTTP error occurred during scene search request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)

    @mock.patch('usgs.api.requests.Session.post', MockPost(status_code=500, reason="Server Error"))
    @mock.patch('usgs.api.os.remove')
    @mock.patch('usgs.api.os.path.exists', return_value=True)
    def test_logout_http_error(self, mock_exists, mock_remove):
        with self.assertRaises(USGSError) as cm:
            api.logout()
        assert "HTTP error occurred during logout request" in str(cm.exception)
        assert isinstance(cm.exception.__cause__, requests.HTTPError)
        # credentials file is always removed on logout, even when the request fails
        mock_remove.assert_called_once()
