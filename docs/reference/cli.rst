.. module:: usgs.scripts

.. cli:

USGS CLI
========

This library comes with a command line interface to expose many common requests, such as authenticating, searching, downloading, and obtaining metadata.

Here's an example of what can be done using the cli and GitHub Gists.

.. code-block:: bash

    usgs search --node EE EO1_HYP_PUB --start-date 20150401 --end-date 20150501 --geojson | gist -f hyperion-20150401-20150501.geojson

.. raw:: html

    <div style="margin-top:10px; margin-bottom:20px">
      <iframe class='ghmap' width="640" height="400" src="https://render.githubusercontent.com/view/geojson/?url=https%3A%2F%2Fgist.githubusercontent.com%2Fkapadia%2F6e722427cecd9ac79971%2Fraw%2Fhyperion-20150401-20150501.geojson#aa859151-d85a-414d-865c-9704fae891a1" frameborder="0"></iframe>
    </div>


Login
-----

.. code-block:: bash

    usgs login [USGS username] [USGS password]

Logout
------

.. code-block:: bash

    usgs logout [USGS username] [USGS password]

Search
------

.. code-block:: bash

    usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat] --node [node]

Suppose you're interested in declassified satellite imagery. The datasets ``CORONA2`` or ``DECLASSII`` can be queried. If you have a GeoJSON file with an AOI, you can pipe the file to ``usgs search``.

.. code-block:: bash

    cat chile.geojson | usgs search --node EE DECLASSII --start-date 19700101 --end-date 19800101 --geojson | gist -f declassii-chile-1970s.geojson

.. raw:: html

    <div style="margin-top:10px; margin-bottom:20px">
      <iframe class='ghmap' width="640" height="400" src="https://render.githubusercontent.com/view/geojson/?url=https%3A%2F%2Fgist.githubusercontent.com%2Fkapadia%2Ffd15d4082da2ec47dbc5%2Fraw%2Fdeclassii-chile-1970s.geojson#08b6ad6d-046d-4fac-9ada-553356358235" frameborder="0"></iframe>
    </div>
    
    <script>
    window.onresize = function(e) {
      var mainEl = document.querySelector('div[role="main"]');
      
      var mapElems = document.querySelectorAll('.ghmap');
      for (var i = 0; i < mapElems.length; i++) {
        mapElems[i].width = mainEl.clientWidth;
      }
    }
    
    window.onresize();
    </script>


Metadata
--------

.. code-block:: bash

    usgs metadata [dataset] [entity/scene id 1] [entity/scene id 2] ... [entity/scene id n]

Suppose you want metadata from a couple scenes taken by Hyperion.

.. code-block:: bash

    $ usgs metadata --node EE EO1_HYP_PUB EO1H1820422014302110K2_SG1_01 EO1H1830422015093110KF_TR2_01 | jq ""
    {
      "errorCode": null,
      "executionTime": 1.676698923111,
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
        },
        {
          "metadataUrl": "https://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1830422015093110KF_TR2_01/",
          "upperLeftCoordinate": {
            "latitude": 25.663285,
            "longitude": 20.41565
          },
          "fgdcMetadataUrl": "https://earthexplorer.usgs.gov/fgdc/1854/EO1H1830422015093110KF_TR2_01/save_xml",
          "displayId": "EO1H1830422015093110KF_TR2_01",
          "acquisitionDate": "2015-04-03",
          "browseUrl": "https://earthexplorer.usgs.gov/browse/eo-1/hyp/183/42/2015/EO11830422015093110KF_TR2_01.jpeg",
          "dataAccessUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
          "orderUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
          "upperRightCoordinate": {
            "latitude": 25.650833,
            "longitude": 20.489455
          },
          "summary": "Entity ID: EO1H1830422015093110KF_TR2_01, Acquisition Date: 03-APR-15, Target Path: 183, Target Row: 42",
          "downloadUrl": "https://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1830422015093110KF_TR2_01/INVSVC/",
          "lowerLeftCoordinate": {
            "latitude": 24.800065,
            "longitude": 20.220225
          },
          "modifiedDate": "2017-03-22",
          "startTime": "2015-04-03",
          "sceneBounds": "20.220225,24.787699,20.489455,25.663285",
          "ordered": false,
          "entityId": "EO1H1830422015093110KF_TR2_01",
          "endTime": "2015-04-03",
          "lowerRightCoordinate": {
            "latitude": 24.787699,
            "longitude": 20.293527
          },
          "bulkOrdered": false
        }
      ],
      "api_version": "1.2.1",
      "error": ""
    }

Unfortunately, this is not all the metadata available for each scene. More metadata is found behind the ``metadataUrl``. Using the ``extended`` flag will send a second request to USGS, and aggregrate the results in the returned JSON.

.. code-block:: bash

    $ usgs metadata --node EE EO1_HYP_PUB EO1H1820422014302110K2_SG1_01 EO1H1830422015093110KF_TR2_01 --extended | jq ""
    {
      "errorCode": null,
      "executionTime": 1.5633571147919,
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
          "extended": {
            "NE Corner Long": "21&amp;deg;35'20.41&quot;E",
            "NW Corner Long": "21&amp;deg;30'58.05&quot;E",
            "Entity ID": "EO1H1820422014302110K2_SG1_01",
            "Sun Elevation": "38.506879",
            "NW Corner Lat dec": "26.178639",
            "Station": "SG1",
            "Center Latitude dec": "25.233517",
            "Target Path": "182",
            "SE Corner Long": "21&amp;deg;08'06.46&quot;E",
            "Look Angle": "2.2046",
            "SW Corner Long dec": "21.063363",
            "Scene Start Time": "2014:302:07:58:59.273",
            "Cloud Cover": "10% to 19% Cloud Cover",
            "NW Corner Lat": "26&amp;deg;10'43.10&quot;N",
            "SW Corner Lat dec": "24.302885",
            "Orbit Row": "42",
            "NE Corner Lat": "26&amp;deg;09'50.63&quot;N",
            "Target Row": "42",
            "Date Entered": "2014/10/29",
            "NW Corner Long dec": "21.516126",
            "Processing Level": "L1T Product Available",
            "Center Longtude dec": "21.325905",
            "NE Corner Lat dec": "26.164064",
            "SE Corner Long dec": "21.135127",
            "Center Latitude": "25&amp;deg;14'00.66&quot;N",
            "SW Corner Long": "21&amp;deg;03'48.11&quot;E",
            "NE Corner Long dec": "21.589002",
            "SE Corner Lat dec": "24.288481",
            "Acquisition Date": "2014/10/29",
            "Scene Stop Time": "2014:302:07:59:31.273",
            "SE Corner Lat": "24&amp;deg;17'18.53&quot;N",
            "Satellite Inclination": "97.96",
            "Orbit Path": "182",
            "Center Longitude": "21&amp;deg;19'33.26&quot;E",
            "SW Corner Lat": "24&amp;deg;18'10.39&quot;N",
            "Sun Azimuth": "134.735736"
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
        },
        {
          "metadataUrl": "https://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1830422015093110KF_TR2_01/",
          "upperLeftCoordinate": {
            "latitude": 25.663285,
            "longitude": 20.41565
          },
          "fgdcMetadataUrl": "https://earthexplorer.usgs.gov/fgdc/1854/EO1H1830422015093110KF_TR2_01/save_xml",
          "displayId": "EO1H1830422015093110KF_TR2_01",
          "acquisitionDate": "2015-04-03",
          "browseUrl": "https://earthexplorer.usgs.gov/browse/eo-1/hyp/183/42/2015/EO11830422015093110KF_TR2_01.jpeg",
          "dataAccessUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
          "orderUrl": "https://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
          "upperRightCoordinate": {
            "latitude": 25.650833,
            "longitude": 20.489455
          },
          "summary": "Entity ID: EO1H1830422015093110KF_TR2_01, Acquisition Date: 03-APR-15, Target Path: 183, Target Row: 42",
          "downloadUrl": "https://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1830422015093110KF_TR2_01/INVSVC/",
          "lowerLeftCoordinate": {
            "latitude": 24.800065,
            "longitude": 20.220225
          },
          "extended": {
            "NE Corner Long": "20&amp;deg;28'20.11&quot;E",
            "NW Corner Long": "20&amp;deg;23'52.21&quot;E",
            "Entity ID": "EO1H1830422015093110KF_TR2_01",
            "Sun Elevation": "42.984461",
            "NW Corner Lat dec": "25.587842",
            "Station": "TR2",
            "Center Latitude dec": "25.15576",
            "Target Path": "183",
            "SE Corner Long": "20&amp;deg;16'43.78&quot;E",
            "Look Angle": "-10.588",
            "SW Corner Long dec": "20.20492",
            "Scene Start Time": "2015:093:07:44:06.278",
            "Cloud Cover": "0 to 9% Cloud Cover",
            "NW Corner Lat": "25&amp;deg;35'16.23&quot;N",
            "SW Corner Lat dec": "24.737627",
            "Orbit Row": "43",
            "NE Corner Lat": "25&amp;deg;34'25.92&quot;N",
            "Target Row": "42",
            "Date Entered": "2015/04/03",
            "NW Corner Long dec": "20.397836",
            "Processing Level": "L1T Product Available",
            "Center Longtude dec": "20.33846",
            "NE Corner Lat dec": "25.573867",
            "SE Corner Long dec": "20.278828",
            "Center Latitude": "25&amp;deg;09'20.74&quot;N",
            "SW Corner Long": "20&amp;deg;12'17.71&quot;E",
            "NE Corner Long dec": "20.472254",
            "SE Corner Lat dec": "24.723703",
            "Acquisition Date": "2015/04/03",
            "Scene Stop Time": "2015:093:07:44:21.278",
            "SE Corner Lat": "24&amp;deg;43'25.33&quot;N",
            "Satellite Inclination": "97.98",
            "Orbit Path": "182",
            "Center Longitude": "20&amp;deg;20'18.46&quot;E",
            "SW Corner Lat": "24&amp;deg;44'15.46&quot;N",
            "Sun Azimuth": "107.463027"
          },
          "modifiedDate": "2017-03-22",
          "startTime": "2015-04-03",
          "sceneBounds": "20.220225,24.787699,20.489455,25.663285",
          "ordered": false,
          "entityId": "EO1H1830422015093110KF_TR2_01",
          "endTime": "2015-04-03",
          "lowerRightCoordinate": {
            "latitude": 24.787699,
            "longitude": 20.293527
          },
          "bulkOrdered": false
        }
      ],
      "api_version": "1.2.1",
      "error": ""
    }


Download Options
----------------
  
.. code-block:: bash

    usgs download-options [dataset] [entity/scene id] --node [node]

Download URL
------------
    
.. code-block:: bash

    usgs download-url [dataset] [entity/scene id] --node [node] --product [product]
