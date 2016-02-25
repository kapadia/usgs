
import os
import pytest
import mock

from usgs import api
from .fakes import FakePostMetadata, FakeDataSets, FakeDataSetsFields


def test_clear_bulk_download_order():
    pytest.skip()


def test_clear_order():
    pytest.skip()


@mock.patch('usgs.api.requests.post', FakeDataSets)
def test_datasets():

    expected_keys = [
        "bounds", "datasetName", "datasetFullName",
        "endDate", "startDate", "supportDownload",
        "supportBulkDownload", "bulkDownloadOrderLimit",
        "supportOrder", "orderLimit", "totalScenes"
    ]

    results = api.datasets(None, "EE")
    for item in results:
        for key in expected_keys:
            assert item.get(key) is not None


@mock.patch('usgs.api.requests.post', FakeDataSetsFields)
def test_dataset_fields():

    expected_keys = ["fieldId", "name", "valueList", "fieldLink"]

    results = api.dataset_fields("LANDSAT_8", "EE")
    for item in results:
        for key in expected_keys:
            assert item.get(key) is not None


def test_download():
    pytest.skip()


def test_download_options():
    pytest.skip()


def test_get_bulk_download_products():
    pytest.skip()


def test_get_order_products():
    pytest.skip()


def test_hits():
    pytest.skip()


def test_item_basket():
    pytest.skip()


@pytest.mark.skipif(os.environ.get("USGS_USERNAME") is None, reason="requires USGS credentials")
@pytest.mark.skipif(os.environ.get("USGS_PASSWORD") is None, reason="requires USGS credentials")
def test_login():

    username = os.environ.get("USGS_USERNAME")
    password = os.environ.get("USGS_PASSWORD")
    api_key = api.login(username, password)

    assert isinstance(api_key, str)


@pytest.mark.skipif(not os.path.exists(os.path.join("/", "tmp", "usgs")), reason="requires USGS credentials")
def test_logout():
    assert api.logout()


@mock.patch('usgs.api.requests.post', FakePostMetadata)
def test_metadata():

    expected_keys = [
        "acquisitionDate", "startTime", "endTime",
        "lowerLeftCoordinate", "upperLeftCoordinate",
        "upperRightCoordinate", "lowerRightCoordinate",
        "sceneBounds", "browseUrl", "dataAccessUrl",
        "downloadUrl", "entityId", "metadataUrl",
        "modifiedDate", "summary"
    ]

    results = api.metadata("LANDSAT_8", "EE", "LC80360332014357LGN00")
    for item in results:
        for key in expected_keys:
            assert item.get(key) is not None


def test_remove_bulk_download_scene():
    pytest.skip()


def test_remove_order_scene():
    pytest.skip()


def test_search_request():
    pytest.skip()


def test_submit_bulk_order():
    pytest.skip()


def test_submit_order():
    pytest.skip()


def test_update_bulk_download_scene():
    pytest.skip()


def test_update_order_scene():
    pytest.skip()


