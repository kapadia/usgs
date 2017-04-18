.. module:: usgs

.. api:

USGS API
=============

Examples
********

The ``where`` parameter used for searching a USGS dataset is best understood by example.

.. code-block:: python


    from usgs import api


    def submit_where_query():

        # USGS uses numerical codes to identify queryable fields
        # To see which fields are queryable for a specific dataset,
        # send off a request to dataset-fields

        results = api.dataset_fields('LANDSAT_8_C1', 'EE')

        for field in results['data']:
            print field

        # WRS Path happens to have the field id 20514
        where = {
            20514: '043'
        }
        results = api.search('LANDSAT_8_C1', 'EE', where=where, start_date='2017-04-01', end_date='2017-05-01', max_results=10, extended=True)

        for scene in results['data']['results']:
            print scene


.. automodule:: usgs.api
	:members: