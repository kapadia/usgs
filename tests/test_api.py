import pytest
import mock

from usgs import api
from .MockPost import MockPost


def check_root_keys(response):

    expected_keys = ["errorCode", "executionTime", "data", "api_version", "error"]
    for key in expected_keys:
        if key not in response:
            return False

    return True


def test_clear_bulk_download_order():
    pytest.skip()


def test_clear_order():
    pytest.skip()


@mock.patch('usgs.api.requests.post', MockPost('dataset-fields.json'))
def test_dataset_fields():

    expected_keys = ["fieldId", "name", "valueList", "fieldLink"]
    response = api.dataset_fields("LANDSAT_8_C1", "EE")

    assert check_root_keys(response)

    for item in response['data']:
        for key in expected_keys:
            assert item.get(key) is not None


@mock.patch('usgs.api.requests.post', MockPost('datasets.json'))
def test_datasets():

    expected_keys = [
        "bounds", "datasetName", "datasetFullName",
        "endDate", "startDate", "supportDownload",
        "supportBulkDownload", "bulkDownloadOrderLimit",
        "supportOrder", "orderLimit", "totalScenes"
    ]
    response = api.datasets(None, "EE")

    assert check_root_keys(response)

    for item in response['data']:
        for key in expected_keys:
            assert item.get(key) is not None


@mock.patch('usgs.api.requests.post', MockPost('download.json'))
def test_download():
    response = api.download("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"], product='STANDARD')
    assert check_root_keys(response)
    assert len(response['data']) == 1


@mock.patch('usgs.api.requests.post', MockPost('download-options.json'))
def test_download_options():

    expected_keys = ["available", "storageLocation", "url", "productName", "filesize", "downloadCode"]
    response = api.download_options("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"])

    assert check_root_keys(response)

    for item in response["data"][0]["downloadOptions"]:
        for key in expected_keys:
            assert item.get(key) is not None


def test_get_bulk_download_products():
    pytest.skip()


def test_get_order_products():
    pytest.skip()


def test_hits():
    pytest.skip()


def test_item_basket():
    pytest.skip()


@mock.patch('usgs.api.requests.post', MockPost('metadata.json'))
def test_metadata():

    expected_keys = [
        "acquisitionDate", "startTime", "endTime",
        "lowerLeftCoordinate", "upperLeftCoordinate",
        "upperRightCoordinate", "lowerRightCoordinate",
        "sceneBounds", "browseUrl", "dataAccessUrl",
        "downloadUrl", "entityId", "metadataUrl",
        "modifiedDate", "summary"
    ]

    response = api.metadata("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"])
    assert check_root_keys(response)

    for item in response['data']:
        for key in expected_keys:
            assert item.get(key) is not None


def test_remove_bulk_download_scene():
    pytest.skip()


def test_remove_order_scene():
    pytest.skip()


@mock.patch('usgs.api.requests.post', MockPost('search.json'))
def test_search():
    expected_keys = ["totalHits", "firstRecord", "nextRecord", "results", "numberReturned", "lastRecord"]

    response = api.search("LANDSAT_8_C1", "EE", start_date='20170401', end_date='20170402', max_results=10)
    assert check_root_keys(response)

    assert len(response['data']["results"]) == 10

    data = response['data']
    for key in expected_keys:
        assert key in data

