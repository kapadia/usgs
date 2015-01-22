.. module:: usgs.scripts

.. cli:

USGS CLI
========

This library comes with a command line interface to expose many common requests, such as authenticating, searching, downloading, and obtaining metadata.

.. code-block:: bash

    usgs login [USGS username] [USGS password]

.. code-block:: bash

    usgs logout [USGS username] [USGS password]

.. code-block:: bash

    usgs search [dataset] --start-date [start date] --end-date [end date] --longitude [lng] --latitude [lat] --node [node]

.. code-block:: bash

    usgs metadata [dataset] [entity/scene id 1] [entity/scene id 2] ... [entity/scene id n]
  
.. code-block:: bash

    usgs download-options [dataset] [entity/scene id] --node [node]
    
.. code-block:: bash

    usgs download-url [dataset] [entity/scene id] --node [node] --product [product]