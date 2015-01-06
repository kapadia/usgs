
========
USGS API
========

.. image:: https://travis-ci.org/mapbox/usgs.svg
   :target: https://travis-ci.org/mapbox/usgs

.. image:: https://coveralls.io/repos/mapbox/usgs/badge.png
   :target: https://coveralls.io/r/mapbox/usgs
   

USGS is a python module for interfacing with the US Geological Survey's API. It provides submodules to interact with various endpoints, and command line utilities, helpful for building out large pipelines.

USGS CLI
========

Available commands are shown with

.. code-block:: pycon

  $ usgs

Help for a command is shown with 

.. code-block:: pycon

  $ usgs [command] --help

------
Search
------

Searching USGS may be done by date or location.

.. code-block:: pycon

    $ usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat]

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

