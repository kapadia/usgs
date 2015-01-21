usgs
====

usgs is a Python library for interfacing with the US Geologic Survey's Inventory Service. The Inventory Service supports a variety of requests for accessing USGS datasets, including searching datasets, downloading data products, and accessing metadata on data products.

Contents:

.. toctree::
   :maxdepth: 2
   
   reference/cli
   reference/api
   reference/soap
   reference/catalog/cwic
   reference/catalog/ee
   reference/catalog/hdds

Catalogs
--------

USGS organizes datasets into four catalogs. Each catalog is specified by a node value. All requests made to the Inventory Service must have an associated node.

+-------------------+-------------------+----------------------------------+
| Catalog           | Node Value        | URI                              |
+===================+===================+==================================+
| CWIC/LSI Explorer | CWIC              | http://lsiexplorer.cr.usgs.gov   |
+-------------------+-------------------+----------------------------------+
| EarthExplorer     | EE                | http://earthexplorer.usgs.gov    |
+-------------------+-------------------+----------------------------------+
| HDDSExplorer      | HDDS              | http://hddsexplorer.usgs.gov     |
+-------------------+-------------------+----------------------------------+
| LPVSExplorer      | LPVS              | http://lpvsexplorer.cr.usgs.gov/ |
+-------------------+-------------------+----------------------------------+


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`