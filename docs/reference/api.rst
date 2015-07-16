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

        fields = api.dataset_fields('LANDSAT_8', 'EE')

        for field in fields:
            print field

        # WRS Path happens to have the field id 10036
        where = {
            10036: '043'
        }
        scenes = api.search('LANDSAT_8', 'EE', where=where, start_date='2015-04-01', end_date='2015-05-01', max_results=10, extended=True)

        for scene in scenes:
            print scene


.. automodule:: usgs.api
	:members: