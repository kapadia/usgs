usgs
====

usgs is a Python library for interfacing with the US Geologic Survey's Inventory Service. The Inventory Service supports a variety of requests for accessing USGS datasets, including searching datasets, downloading data products, and accessing metadata on data products.


.. note:: All requests require an account with `USGS's EROS service <https://ers.cr.usgs.gov/register/>`_. The account must also have Machine to Machine privileges.

.. note:: As of May 15, 2017 the USGS has deprecated their SOAP API. This library has been updated to use their JSON API. As a result most, if not all, responses through this client will have a different structure compared to the older SOAP version.

.. note:: This library currently uses version 1.4 of the USGS Inventory Service API.


Installation
------------

.. code-block:: bash

    pip install usgs


Examples
--------

These two examples demonstrate how to access metadata for a Hyperion scene and Landsat 8 scene. Both datasets are part of the EarthExplorer catalog. Hyperion is designated by the dataset ``EO1_HYP_PUB``, Landsat 8 is designated by ``LANDSAT_8``.


Python
******

.. code-block:: python

    from usgs import api
    
    # Set the EarthExplorer catalog
    node = 'EE'
    
    # Set the Hyperion and Landsat 8 dataset
    hyperion_dataset = 'EO1_HYP_PUB'
    landsat8_dataset = 'LANDSAT_8'
    
    # Set the scene ids
    hyperion_scene_id = 'EO1H1820422014302110K2_SG1_01'
    landsat8_scene_id = 'LC80290462015135LGN00'
    
    # Submit requests to USGS servers
    api.metadata(hyperion_dataset, node, [hyperion_scene_id])
    api.metadata(landsat8_dataset, node, [landsat8_scene_id])


Command Line
************

.. code-block:: bash

    $ usgs metadata --node EE EO1_HYP_PUB EO1H1820422014302110K2_SG1_01
    {
      "errorCode": null,
      "executionTime": 1.6408669948578,
      "data": [
        {
          "metadataUrl": "https://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1820422014302110K2_SG1_01/",
          "upperLeftCoordinate": {
            "latitude": 26.253489,
            "longitude": 21.53022
          },
          "fgdcMetadataUrl": "https://earthexplorer.usgs.gov/fgdc/1854/EO1H1820422014302110K2_SG1_01/save_xml",
          "displayId": "EO1H1820422014302110K2_SG1_01",
          "acquisitionDate": "2014-10-29",
          "browseUrl": "https://earthexplorer.usgs.gov/browse/eo-1/hyp/182/42/2014/EO11820422014302110K2_SG1_01.jpeg",
          "dataAccessUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
          "orderUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
          "upperRightCoordinate": {
            "latitude": 26.240475,
            "longitude": 21.602509
          },
          "summary": "Entity ID: EO1H1820422014302110K2_SG1_01, Acquisition Date: 29-OCT-14, Target Path: 182, Target Row: 42",
          "downloadUrl": "https://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1820422014302110K2_SG1_01/INVSVC/",
          "lowerLeftCoordinate": {
            "latitude": 24.365584,
            "longitude": 21.074194
          },
          "modifiedDate": "2017-03-22",
          "startTime": "2014-10-29",
          "sceneBounds": "21.074194,24.352528,21.602509,26.253489",
          "ordered": false,
          "entityId": "EO1H1820422014302110K2_SG1_01",
          "endTime": "2014-10-29",
          "lowerRightCoordinate": {
            "latitude": 24.352528,
            "longitude": 21.145425
          },
          "bulkOrdered": false
        }
      ],
      "api_version": "1.2.1",
      "error": ""
    }
    
    $ usgs metadata --node EE LANDSAT_8 LC80290462015135LGN00
    {
      "errorCode": null,
      "executionTime": 1.7327969074249,
      "data": [
        {
          "metadataUrl": "https://earthexplorer.usgs.gov/metadata/xml/4923/LC80290462015135LGN00/",
          "upperLeftCoordinate": {
            "latitude": 21.27723,
            "longitude": -104.10944
          },
          "fgdcMetadataUrl": "https://earthexplorer.usgs.gov/fgdc/4923/LC80290462015135LGN00/save_xml",
          "displayId": "LC80290462015135LGN00",
          "acquisitionDate": "2015-05-15",
          "browseUrl": "https://earthexplorer.usgs.gov/browse/landsat_8/2015/029/046/LC80290462015135LGN00.jpg",
          "dataAccessUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=LANDSAT_8&ordered=LC80290462015135LGN00&node=INVSVC",
          "orderUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=LANDSAT_8&ordered=LC80290462015135LGN00&node=INVSVC",
          "upperRightCoordinate": {
            "latitude": 20.90999,
            "longitude": -102.32534
          },
          "summary": "Entity ID: LC80290462015135LGN00, Acquisition Date: 15-MAY-15, Path: 29, Row: 46",
          "downloadUrl": "https://earthexplorer.usgs.gov/download/external/options/LANDSAT_8/LC80290462015135LGN00/INVSVC/",
          "lowerLeftCoordinate": {
            "latitude": 19.54002,
            "longitude": -104.50364
          },
          "modifiedDate": "2017-02-07",
          "startTime": "2015-05-15",
          "sceneBounds": "-104.50364,19.17102,-102.32534,21.27723",
          "ordered": false,
          "entityId": "LC80290462015135LGN00",
          "endTime": "2015-05-15",
          "lowerRightCoordinate": {
            "latitude": 19.17102,
            "longitude": -102.73968
          },
          "bulkOrdered": false
        }
      ],
      "api_version": "1.2.1",
      "error": ""
    }


Catalogs
--------

USGS provides four catalogs, each containing various datasets. All requests made to the Inventory Service must have an associated node.

Check each catalog for a list of datasets.

+--------------+------------+----------------------------------+
| Catalog      | Node Value | URI                              |
+==============+============+==================================+
| :ref:`cwic`  | CWIC       | http://lsiexplorer.cr.usgs.gov   |
+--------------+------------+----------------------------------+
| :ref:`ee`    | EE         | http://earthexplorer.usgs.gov    |
+--------------+------------+----------------------------------+
| :ref:`hdds`  | HDDS       | http://hddsexplorer.usgs.gov     |
+--------------+------------+----------------------------------+
| :ref:`lpcs`  | LPCS       | http://lpcsexplorer.cr.usgs.gov  |
+--------------+------------+----------------------------------+

Contents:

.. toctree::
   :maxdepth: 2
   
   reference/cli
   reference/api
   reference/payloads
   reference/catalog/cwic
   reference/catalog/ee
   reference/catalog/hdds
   reference/catalog/lpcs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`