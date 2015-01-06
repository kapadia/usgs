
========
USGS API
========

.. image:: https://travis-ci.org/mapbox/usgs.svg
   :target: https://travis-ci.org/mapbox/usgs

.. image:: https://coveralls.io/repos/mapbox/usgs/badge.png
   :target: https://coveralls.io/r/mapbox/usgs
   

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


USGS CLI
========

Available commands are shown with

.. code-block:: pycon

  $ usgs

Help for a specific command is shown with 

.. code-block:: pycon

  $ usgs [command] --help

------
Search
------

Searching USGS may be done by date, location or both.

.. code-block:: pycon

    $ usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat] --node [node]

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

