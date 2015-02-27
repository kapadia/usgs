usgs
====

usgs is a Python library for interfacing with the US Geologic Survey's Inventory Service. The Inventory Service supports a variety of requests for accessing USGS datasets, including searching datasets, downloading data products, and accessing metadata on data products.


.. note:: Some requests require an account with `USGS's EROS service <https://earthexplorer.usgs.gov/register/>`_. The account must also have Machine to Machine privileges.

Installation
------------

.. todo:: Post on PyPI

.. code-block:: bash

    pip install git+https://github.com/mapbox/usgs.git


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
| LPVSExplorer | LPVS       | http://lpvsexplorer.cr.usgs.gov/ |
+--------------+------------+----------------------------------+

Contents:

.. toctree::
   :maxdepth: 2
   
   reference/cli
   reference/api
   reference/soap
   reference/catalog/cwic
   reference/catalog/ee
   reference/catalog/hdds


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`