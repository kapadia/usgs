
import os
import json
import click
from datetime import datetime
from usgs import api


def to_coordinates(bounds):
    xmin, ymin, xmax, ymax = bounds
    
    return [[
        [xmin, ymin],
        [xmin, ymax],
        [xmax, ymax],
        [xmax, ymin],
        [xmin, ymin]
    ]]


def to_geojson_feature(entry):

    # TODO: This key may not be present in all datasets.
    bounds = map(float, entry.pop("sceneBounds").split(','))

    coordinates = to_coordinates(bounds)

    return {
        "type": "Feature",
        "properties": entry,
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        }
    }


def to_geojson(result):
    gj = {
        'type': 'FeatureCollection'
    }

    if type(result['data']) is list:
        features = map(to_geojson_feature, result['data'])
    else:
        features = map(to_geojson_feature, result['data']['results'])
        for key in result['data']:
            if key == "results":
                continue
            gj[key] = result['data'][key]

    gj['features'] = features
    for key in result:
        if key == "data":
            continue
        gj[key] = result[key]

    return gj


def explode(coords):
    for e in coords:
        if isinstance(e, (float, int)):
            yield coords
            break
        else:
            for f in explode(e):
                yield f

def get_bbox(f):
    x, y = zip(*list(explode(f['geometry']['coordinates'])))
    return min(x), min(y), max(x), max(y)


api_key_opt = click.option("--api-key", help="API key returned from USGS servers after logging in.", default=None)
catalog_opt = click.option("--catalog", help="The catalog corresponding to the dataset. One of EE or HDDS).", default=None, type=click.Choice(['EE', 'HDDS']))
dataset_opt = click.option("--dataset", help="The name of a dataset, e.g. landsat_8_c1")
start_date_opt = click.option("--start-date", default=None, help="The start date of a dataset or acquisition")
end_date_opt = click.option("--end-date", default=None, help="The start date of a dataset or acquisition")

@click.group()
def usgs():
    pass

@click.command()
@click.argument("username", envvar='USGS_USERNAME')
@click.argument("password", envvar='USGS_PASSWORD')
def cycle_token(username, password):

    credential_filepath = os.path.join(os.path.expanduser("~"), ".usgs")
    with open(credential_filepath) as f:
        credentials = json.load(f)

    created = datetime.strptime(credentials['created'], "%Y-%m-%dT%H:%M:%S.%f")
    token_lifetime = (datetime.now() - created).seconds
    approx_two_hours = 2 * 60 * 60 - 60
    click.echo('The token lifetime is {} seconds'.format(token_lifetime))
    if token_lifetime > approx_two_hours:
        api.logout()
        api.login(username, password)


@click.command()
@click.argument("dataset")
def dataset_filters(dataset):
    data = api.dataset_filters(dataset)
    click.echo(json.dumps(data))


@click.command()
@catalog_opt
@dataset_opt
@start_date_opt
@end_date_opt
def dataset_search(catalog, dataset, start_date, end_date):
    data = api.dataset_search(
        dataset=dataset, catalog=catalog, start_date=start_date, end_date=end_date)
    click.echo(json.dumps(data))


@click.command()
@click.argument("dataset")
@click.argument("scene-ids", nargs=-1)
@api_key_opt
def download_options(dataset, scene_ids, api_key):
    data = api.download_options(dataset, scene_ids)
    click.echo(json.dumps(data))


@click.command()
@click.argument("dataset")
@click.argument("entity_id")
@click.option("--product-id", required=True)
@api_key_opt
def download_request(dataset, entity_id, product_id, api_key):
    data = api.download_request(dataset, entity_id, product_id)
    click.echo(json.dumps(data))


@click.command()
@click.argument("username", envvar='USGS_USERNAME')
@click.argument("password", envvar='USGS_PASSWORD')
def login(username, password):
    click.echo(api.login(username, password))


@click.command()
def logout():
    click.echo(api.logout())


@click.command()
@click.argument("dataset")
@click.argument("scene-id", nargs=1)
@click.option('--geojson', is_flag=True)
@api_key_opt
def scene_metadata(dataset, scene_id, geojson, api_key):
    result = api.scene_metadata(dataset, scene_id, api_key=api_key)

    if geojson:
        result = to_geojson(result)

    click.echo(json.dumps(result))


@click.command()
@click.argument("dataset")
@click.argument("aoi", default="-", required=False)
@click.option('--max-results', default=5000, type=int)
@click.option('--metadata-type', type=click.Choice(['summary', 'full']))
@click.option("--start-date")
@click.option("--end-date")
@click.option("--lower-left", nargs=2, help="Longitude/latitude specifying the lower left of the search window")
@click.option("--upper-right", nargs=2, help="Longitude/latitude specifying the lower left of the search window")
@click.option("--longitude", type=float)
@click.option("--latitude", type=float)
@click.option("--distance", type=float, help="Radius - in units of meters - used to search around the specified longitude/latitude.", default=100)
@click.option("--where", nargs=2, multiple=True, help="Supply additional search criteria.")
@api_key_opt
def scene_search(
    dataset, aoi, max_results, metadata_type,
    start_date, end_date, lower_left, upper_right,
    longitude, latitude, distance,
    where, api_key):

    if aoi:
        src = click.open_file('-') if aoi == "-" else click.open_file(aoi)
        if not src.isatty():
            lines = src.readlines()
            if len(lines) > 0:
                aoi = json.loads(''.join([ line.strip() for line in lines ]))
                bbox = [
                    get_bbox(feature) for feature in aoi.get('features')
                ][0]
                lower_left = bbox[0:2]
                upper_right = bbox[2:4]
    
    if where:
        # Query the dataset fields endpoint for queryable fields
        resp = api.dataset_fields(dataset, node)

        def format_fieldname(s):
            return ''.join(c for c in s if c.isalnum()).lower()

        field_lut = { format_fieldname(field['name']): field['fieldId'] for field in resp['data'] }
        where = { field_lut[format_fieldname(k)]: v for k, v in where if format_fieldname(k) in field_lut }

    if len(lower_left) > 0:
        lower_left = dict(zip(['longitude', 'latitude'], lower_left))
        upper_right = dict(zip(['longitude', 'latitude'], upper_right))
    else:
        lower_left = None
        upper_right = None

    result = api.scene_search(
        dataset, max_results=max_results, metadata_type=metadata_type,
        start_date=start_date, end_date=end_date,
        ll=lower_left, ur=upper_right,
        lng=longitude, lat=latitude, distance=distance)

    print(json.dumps(result))


usgs.add_command(cycle_token, "cycle-token")
usgs.add_command(dataset_filters, "dataset-filters")
usgs.add_command(download_options, "download-options")
usgs.add_command(download_request, "download-request")
usgs.add_command(dataset_search, "dataset-search")
usgs.add_command(login)
usgs.add_command(logout)
usgs.add_command(scene_metadata, "scene-metadata")
usgs.add_command(scene_search, "scene-search")