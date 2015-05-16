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
      <iframe id='ghmap' width="640" height="400" src="https://render.githubusercontent.com/view/geojson/?url=https%3A%2F%2Fgist.githubusercontent.com%2Fkapadia%2F6e722427cecd9ac79971%2Fraw%2Fhyperion-20150401-20150501.geojson#aa859151-d85a-414d-865c-9704fae891a1" frameborder="0"></iframe>
    </div>
    
    <script>
    window.onresize = function(e) {
      var mainEl = document.querySelector('div[role="main"]');
      
      var mapEl = document.getElementById('ghmap');
      mapEl.width = mainEl.clientWidth;
    }
    
    window.onresize();
    </script>


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

Metadata
--------

.. code-block:: bash

    usgs metadata [dataset] [entity/scene id 1] [entity/scene id 2] ... [entity/scene id n]

Suppose you want metadata from a couple scenes taken by Hyperion.

.. code-block:: bash

    $ usgs metadata --node EE EO1_HYP_PUB EO1H1820422014302110K2_SG1_01 EO1H1830422015093110KF_TR2_01 | jq ""
    [
      {
        "bulkOrdered": false,
        "lowerRightCoordinate": {
          "longitude": 21.145425,
          "latitude": 24.352528
        },
        "upperRightCoordinate": {
          "longitude": 21.602509,
          "latitude": 26.240475
        },
        "orderUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
        "dataAccessUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
        "browseUrl": "http://earthexplorer.usgs.gov/browse/eo-1/hyp/182/42/2014/EO11820422014302110K2_SG1_01.jpeg",
        "acquisitionDate": "2014-10-29T00:00:00Z",
        "ordered": false,
        "upperLeftCoordinate": {
          "longitude": 21.53022,
          "latitude": 26.253489
        },
        "metadataUrl": "http://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1820422014302110K2_SG1_01/",
        "summary": "Entity ID: EO1H1820422014302110K2_SG1_01, Acquisition Date: 29-OCT-14, Target Path: 182, Target Row: 42",
        "downloadUrl": "http://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1820422014302110K2_SG1_01/INVSVC/",
        "lowerLeftCoordinate": {
          "longitude": 21.074194,
          "latitude": 24.365584
        },
        "modifiedDate": "2014-11-01T13:18:02Z",
        "startTime": "2014-10-29T07:58:59Z",
        "sceneBounds": "21.074194,24.352528,21.602509,26.253489",
        "entityId": "EO1H1820422014302110K2_SG1_01",
        "endTime": "2014-10-29T07:59:31Z"
      },
      {
        "bulkOrdered": false,
        "lowerRightCoordinate": {
          "longitude": 20.293527,
          "latitude": 24.787699
        },
        "upperRightCoordinate": {
          "longitude": 20.489455,
          "latitude": 25.650833
        },
        "orderUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
        "dataAccessUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
        "browseUrl": "http://earthexplorer.usgs.gov/browse/eo-1/hyp/183/42/2015/EO11830422015093110KF_TR2_01.jpeg",
        "acquisitionDate": "2015-04-03T00:00:00Z",
        "ordered": false,
        "upperLeftCoordinate": {
          "longitude": 20.41565,
          "latitude": 25.663285
        },
        "metadataUrl": "http://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1830422015093110KF_TR2_01/",
        "summary": "Entity ID: EO1H1830422015093110KF_TR2_01, Acquisition Date: 03-APR-15, Target Path: 183, Target Row: 42",
        "downloadUrl": "http://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1830422015093110KF_TR2_01/INVSVC/",
        "lowerLeftCoordinate": {
          "longitude": 20.220225,
          "latitude": 24.800065
        },
        "modifiedDate": "2015-04-07T12:18:01Z",
        "startTime": "2015-04-03T07:44:06Z",
        "sceneBounds": "20.220225,24.787699,20.489455,25.663285",
        "entityId": "EO1H1830422015093110KF_TR2_01",
        "endTime": "2015-04-03T07:44:21Z"
      }
    ]

Unfortunately, this is not all the metadata available for each scene. More metadata is found behind the ``metadataUrl``. Using the ``extended`` flag will send a second request to USGS, and aggregrate the results in the returned JSON.

.. code-block:: bash

    $ usgs metadata --node EE EO1_HYP_PUB EO1H1820422014302110K2_SG1_01 EO1H1830422015093110KF_TR2_01 --extended | jq ""
    [
      {
        "bulkOrdered": false,
        "lowerRightCoordinate": {
          "longitude": 21.145425,
          "latitude": 24.352528
        },
        "endTime": "2014-10-29T07:59:31Z",
        "orderUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
        "dataAccessUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1820422014302110K2_SG1_01&node=INVSVC",
        "browseUrl": "http://earthexplorer.usgs.gov/browse/eo-1/hyp/182/42/2014/EO11820422014302110K2_SG1_01.jpeg",
        "acquisitionDate": "2014-10-29T00:00:00Z",
        "ordered": false,
        "extended": {
          "Sun Azimuth": "134.735736",
          "SW Corner Lat": "24&amp;deg;18'10.39&quot;N",
          "Center Longitude": "21&amp;deg;08'06.46&quot;E",
          "Orbit Path": "182",
          "Orbit Row": "42",
          "SW Corner Lat dec": "24.302885",
          "NW Corner Lat": "26&amp;deg;10'43.10&quot;N",
          "Cloud Cover": "10% to 19% Cloud Cover",
          "Scene Start Time": "2014:302:07:58:59.273",
          "SW Corner Long dec": "21.063363",
          "Look Angle": "2.2046",
          "SE Corner Long": "21&amp;deg;08'06.46&quot;E",
          "NE Corner Long": "21&amp;deg;35'20.41&quot;E",
          "NW Corner Long": "21&amp;deg;30'58.05&quot;E",
          "Entity ID": "EO1H1820422014302110K2_SG1_01",
          "Sun Elevation": "38.506879",
          "NW Corner Lat dec": "26.178639",
          "Station": "SG1",
          "Center Latitude dec": "24.288481",
          "Target Path": "182",
          "NE Corner Lat": "26&amp;deg;09'50.63&quot;N",
          "Target Row": "42",
          "Date Entered": "2014/10/29",
          "NW Corner Long dec": "21.516126",
          "Processing Level": "L1T Product Available",
          "Center Longtude dec": "21.135127",
          "NE Corner Lat dec": "26.164064",
          "SE Corner Long dec": "21.135127",
          "Center Latitude": "24&amp;deg;17'18.53&quot;N",
          "SW Corner Long": "21&amp;deg;03'48.11&quot;E",
          "NE Corner Long dec": "21.589002",
          "SE Corner Lat dec": "24.288481",
          "Acquisition Date": "2014/10/29",
          "Scene Stop Time": "2014:302:07:59:31.273",
          "SE Corner Lat": "24&amp;deg;17'18.53&quot;N",
          "Satellite Inclination": "97.96"
        },
        "upperLeftCoordinate": {
          "longitude": 21.53022,
          "latitude": 26.253489
        },
        "metadataUrl": "http://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1820422014302110K2_SG1_01/",
        "upperRightCoordinate": {
          "longitude": 21.602509,
          "latitude": 26.240475
        },
        "summary": "Entity ID: EO1H1820422014302110K2_SG1_01, Acquisition Date: 29-OCT-14, Target Path: 182, Target Row: 42",
        "downloadUrl": "http://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1820422014302110K2_SG1_01/INVSVC/",
        "lowerLeftCoordinate": {
          "longitude": 21.074194,
          "latitude": 24.365584
        },
        "modifiedDate": "2014-11-01T13:18:02Z",
        "startTime": "2014-10-29T07:58:59Z",
        "sceneBounds": "21.074194,24.352528,21.602509,26.253489",
        "entityId": "EO1H1820422014302110K2_SG1_01"
      },
      {
        "bulkOrdered": false,
        "lowerRightCoordinate": {
          "longitude": 20.293527,
          "latitude": 24.787699
        },
        "endTime": "2015-04-03T07:44:21Z",
        "orderUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
        "dataAccessUrl": "http://earthexplorer.usgs.gov/order/process?dataset_name=EO1_HYP_PUB&ordered=EO1H1830422015093110KF_TR2_01&node=INVSVC",
        "browseUrl": "http://earthexplorer.usgs.gov/browse/eo-1/hyp/183/42/2015/EO11830422015093110KF_TR2_01.jpeg",
        "acquisitionDate": "2015-04-03T00:00:00Z",
        "ordered": false,
        "extended": {
          "Sun Azimuth": "107.463027",
          "SW Corner Lat": "24&amp;deg;44'15.46&quot;N",
          "Center Longitude": "20&amp;deg;16'43.78&quot;E",
          "Orbit Path": "182",
          "Orbit Row": "43",
          "SW Corner Lat dec": "24.737627",
          "NW Corner Lat": "25&amp;deg;35'16.23&quot;N",
          "Cloud Cover": "0 to 9% Cloud Cover",
          "Scene Start Time": "2015:093:07:44:06.278",
          "SW Corner Long dec": "20.20492",
          "Look Angle": "-10.588",
          "SE Corner Long": "20&amp;deg;16'43.78&quot;E",
          "NE Corner Long": "20&amp;deg;28'20.11&quot;E",
          "NW Corner Long": "20&amp;deg;23'52.21&quot;E",
          "Entity ID": "EO1H1830422015093110KF_TR2_01",
          "Sun Elevation": "42.984461",
          "NW Corner Lat dec": "25.587842",
          "Station": "TR2",
          "Center Latitude dec": "24.723703",
          "Target Path": "183",
          "NE Corner Lat": "25&amp;deg;34'25.92&quot;N",
          "Target Row": "42",
          "Date Entered": "2015/04/03",
          "NW Corner Long dec": "20.397836",
          "Processing Level": "L1T Product Available",
          "Center Longtude dec": "20.278828",
          "NE Corner Lat dec": "25.573867",
          "SE Corner Long dec": "20.278828",
          "Center Latitude": "24&amp;deg;43'25.33&quot;N",
          "SW Corner Long": "20&amp;deg;12'17.71&quot;E",
          "NE Corner Long dec": "20.472254",
          "SE Corner Lat dec": "24.723703",
          "Acquisition Date": "2015/04/03",
          "Scene Stop Time": "2015:093:07:44:21.278",
          "SE Corner Lat": "24&amp;deg;43'25.33&quot;N",
          "Satellite Inclination": "97.98"
        },
        "upperLeftCoordinate": {
          "longitude": 20.41565,
          "latitude": 25.663285
        },
        "metadataUrl": "http://earthexplorer.usgs.gov/metadata/xml/1854/EO1H1830422015093110KF_TR2_01/",
        "upperRightCoordinate": {
          "longitude": 20.489455,
          "latitude": 25.650833
        },
        "summary": "Entity ID: EO1H1830422015093110KF_TR2_01, Acquisition Date: 03-APR-15, Target Path: 183, Target Row: 42",
        "downloadUrl": "http://earthexplorer.usgs.gov/download/external/options/EO1_HYP_PUB/EO1H1830422015093110KF_TR2_01/INVSVC/",
        "lowerLeftCoordinate": {
          "longitude": 20.220225,
          "latitude": 24.800065
        },
        "modifiedDate": "2015-04-07T12:18:01Z",
        "startTime": "2015-04-03T07:44:06Z",
        "sceneBounds": "20.220225,24.787699,20.489455,25.663285",
        "entityId": "EO1H1830422015093110KF_TR2_01"
      }
    ]


Download Options
----------------
  
.. code-block:: bash

    usgs download-options [dataset] [entity/scene id] --node [node]
    
Download URL
------------
    
.. code-block:: bash

    usgs download-url [dataset] [entity/scene id] --node [node] --product [product]