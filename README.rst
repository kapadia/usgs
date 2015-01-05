
========
USGS API
========

.. image:: https://travis-ci.org/mapbox/usgs.svg
   :target: https://travis-ci.org/mapbox/usgs

.. image:: https://coveralls.io/repos/mapbox/usgs/badge.png
   :target: https://coveralls.io/r/mapbox/usgs
   

USGS is a python module for interfacing with the US Geological Survey's API. It provides submodules to interact with various endpoints, and command line utilities, helpful for building out large pipelines.

USGS CLI
============

Get metadata for a list of scenes

.. code-block:: pycon
    
    $ usgs metadata [dataset] [scene id 1] [scene id 2] ... [scene id n]


Search USGS for scenes

..code-block:: pycon

    $ usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat]