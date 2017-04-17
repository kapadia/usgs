
import os
import json
from usgs import api

testdir = os.path.dirname(os.path.abspath(__file__))


def write_response(response, filename):
    fpath = os.path.join(testdir, 'data', filename)
    with open(fpath, 'w') as f:
        json.dump(response, f)


def create_snapshots():
    """
    Run requests against USGS API for use in tests.
    """

    api_key = api.login(os.environ['USGS_USERNAME'], os.environ['USGS_PASSWORD'])

    # Dataset Fields
    response = api.dataset_fields("LANDSAT_8_C1", "EE", api_key=api_key)
    write_response(response, 'dataset-fields.json')

    # Datasets
    response = api.datasets(None, "EE")
    write_response(response, 'datasets.json')

    # Download
    response = api.download("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"], product='STANDARD')
    write_response(response, 'download.json')

    # Download Options
    response = api.download_options("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"])
    write_response(response, 'download-options.json')

    # Metadata
    response = api.metadata("LANDSAT_8_C1", "EE", ["LC80810712017104LGN00"])
    write_response(response, 'metadata.json')

    # Search
    response = api.search("LANDSAT_8_C1", "EE", start_date='20170401', end_date='20170402', max_results=10)
    write_response(response, 'search.json')

    api.logout(api_key)


if __name__ == '__main__':
    create_snapshots()
