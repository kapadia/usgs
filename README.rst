
========
USGS API
========

.. image:: https://travis-ci.org/mapbox/usgs.svg
   :target: https://travis-ci.org/mapbox/usgs
   

`USGS` is a python module for interfacing with the US Geological Survey's API. It provides submodules to interact with various endpoints, and command line utilities, helpful for building out large pipelines.

The US Geological Survey divides datasets into four catalogs. This module makes some effort to resolve the node for a given dataset. Sometimes the relationship between dataset and node is ambiguous and must be explicitly specified when requesting data from USGS servers.

+-------------------+-------------------+
| Catalog           | Node Value        |
+===================+===================+
| CWIC/LSI Explorer | CWIC              |
+-------------------+-------------------+
| EarthExplorer     | EE                |
+-------------------+-------------------+
| HDDSExplorer      | HDDS              |
+-------------------+-------------------+
| LPVSExplorer      | LPVS              |
+-------------------+-------------------+

USGS API
========

.. code-block:: python


  # Running through a few examples

  from usgs import api
  
  # username and password are defined somewhere
  api_key = api.login(username, password)
  
  # Get all datasets associated with a node
  earth_explorer_datasets = api.datasets(None, "EE")
  
  # Maybe we only want the full dataset name
  dataset_names = map(lambda ds: ds["datasetFullName"], earth_explorer_datasets)
  
  # Get me some info on recent Landsat 8 scenes.
  scenes = api.search("LANDSAT_8", "EE", lat=30, lng=-70)
  
  # And those juicy scene ids (or entity id)
  scene_ids = map(lambda scene: scene["entityId"], scenes)
  
  # Now I want download URLs for these scenes, and I just happen to know the product type is STANDARD
  urls = api.download("LANDSAT_8", "EE", scene_ids, "STANDARD")


USGS CLI
========

Available commands are shown with

.. code-block:: pycon

  $ usgs

Help for a specific command is shown with 

.. code-block:: pycon

  $ usgs [command] --help

-----
Login
-----

.. code-block:: pycon

    $ usgs login [username] [password]
    
------
Logout
------

.. code-block:: pycon

    $ usgs logout

------
Search
------

Searching USGS may be done by date, location or both.

.. code-block:: pycon

    $ usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat] --node [node]
    
Add the `geojson` flag for GeoJSON output

        $ usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat] --node [node] --geojson

--------
Metadata
--------

.. code-block:: pycon

    $ usgs metadata [dataset] [entity/scene id 1] [entity/scene id 2] ... [entity/scene id n]

----------------
Download Options
----------------

.. code-block:: pycon

    $ usgs download-options [dataset] [entity/scene id] --node [node]

------------
Download URL
------------

.. code-block:: pycon
    
    $ usgs download-url [dataset] [entity/scene id] --node [node] --product [product]

