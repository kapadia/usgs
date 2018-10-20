
import os, json
import click
from usgs import api


def get_node(dataset, node):
    """
    .. todo:: Move to more appropriate place in module.
    """
    
    if node is None:
        
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(cur_dir, "..", "data")
        dataset_path = os.path.join(data_dir, "datasets.json")
        
        with open(dataset_path, "r") as f:
            datasets = json.loads(f.read())
        
        node = datasets[dataset].upper()
    
    return node


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
        if isinstance(e, (float, int, long)):
            yield coords
            break
        else:
            for f in explode(e):
                yield f

def get_bbox(f):
    x, y = zip(*list(explode(f['geometry']['coordinates'])))
    return min(x), min(y), max(x), max(y)


api_key_opt = click.option("--api-key", help="API key returned from USGS servers after logging in.", default=None)
node_opt = click.option("--node", help="The node corresponding to the dataset (CWIC, EE, HDDS, LPVS).", default=None)


@click.group()
def usgs():
    pass


@click.command()
@click.argument("username", envvar='USGS_USERNAME')
@click.argument("password", envvar='USGS_PASSWORD')
def login(username, password):
    api_key = api.login(username, password)
    click.echo(api_key)


@click.command()
def logout():
    click.echo(api.logout())


@click.command()
@click.argument("node")
@click.option("--start-date")
@click.option("--end-date")
def datasets(node, start_date, end_date):
    data = api.datasets(None, node, start_date=start_date, end_date=end_date)
    click.echo(json.dumps(data))


@click.command()
@click.argument("dataset")
@click.argument("scene-ids", nargs=-1)
@node_opt
@click.option("--extended", is_flag=True, help="Probe for more metadata.")
@click.option('--geojson', is_flag=True)
@api_key_opt
def metadata(dataset, scene_ids, node, extended, geojson, api_key):

    if len(scene_ids) == 0:
        scene_ids = map(lambda s: s.strip(), click.open_file('-').readlines())

    node = get_node(dataset, node)
    result = api.metadata(dataset, node, scene_ids, extended=extended, api_key=api_key)

    if geojson:
        result = to_geojson(result)

    click.echo(json.dumps(result))


@click.command()
@click.argument("dataset")
@node_opt
def dataset_fields(dataset, node):
    node = get_node(dataset, node)
    data = api.dataset_fields(dataset, node)
    click.echo(json.dumps(data))


@click.command()
@click.argument("dataset")
@node_opt
@click.argument("aoi", default="-", required=False)
@click.option("--start-date")
@click.option("--end-date")
@click.option("--longitude")
@click.option("--latitude")
@click.option("--distance", help="Radius - in units of meters - used to search around the specified longitude/latitude.", default=100)
@click.option("--lower-left", nargs=2, help="Longitude/latitude specifying the lower left of the search window")
@click.option("--upper-right", nargs=2, help="Longitude/latitude specifying the lower left of the search window")
@click.option("--where", nargs=2, multiple=True, help="Supply additional search criteria.")
@click.option('--max-results', default=None, type=int)
@click.option('--geojson', is_flag=True)
@click.option("--extended", is_flag=True, help="Probe for more metadata.")
@api_key_opt
def search(dataset, node, aoi, start_date, end_date, longitude, latitude, distance, lower_left, upper_right, where, max_results, geojson, extended, api_key):

    node = get_node(dataset, node)
    
    if aoi == "-":
        src = click.open_file('-')
        if not src.isatty():
            lines = src.readlines()
            
            if len(lines) > 0:
                
                aoi = json.loads(''.join([ line.strip() for line in lines ]))
            
                bbox = map(get_bbox, aoi.get('features') or [aoi])[0]
                lower_left = bbox[0:2]
                upper_right = bbox[2:4]
    
    if where:
        # Query the dataset fields endpoint for queryable fields
        resp = api.dataset_fields(dataset, node)

        def format_fieldname(s):
            return ''.join(c for c in s if c.isalnum()).lower()

        field_lut = { format_fieldname(field['name']): field['fieldId'] for field in resp['data'] }
        where = { field_lut[format_fieldname(k)]: v for k, v in where if format_fieldname(k) in field_lut }

    if lower_left:
        lower_left = dict(zip(['longitude', 'latitude'], lower_left))
        upper_right = dict(zip(['longitude', 'latitude'], upper_right))

    result = api.search(
        dataset, node,
        lat=latitude, lng=longitude, distance=distance,
        ll=lower_left, ur=upper_right,
        start_date=start_date, end_date=end_date,
        where=where, max_results=max_results,
        extended=extended, api_key=api_key)

    if geojson:
        result = to_geojson(result)

    print(json.dumps(result))


@click.command()
@click.argument("dataset")
@click.argument("scene-ids", nargs=-1)
@node_opt
@api_key_opt
def download_options(dataset, scene_ids, node, api_key):
    
    node = get_node(dataset, node)
    
    data = api.download_options(dataset, node, scene_ids)
    print(json.dumps(data))


@click.command()
@click.argument("dataset")
@click.argument("scene_ids", nargs=-1)
@click.option("--product", nargs=1, required=True)
@node_opt
@api_key_opt
def download_url(dataset, scene_ids, product, node, api_key):
    
    node = get_node(dataset, node)
    
    data = api.download(dataset, node, scene_ids, product)
    click.echo(json.dumps(data))


usgs.add_command(login)
usgs.add_command(logout)
usgs.add_command(datasets)
usgs.add_command(dataset_fields, "dataset-fields")
usgs.add_command(metadata)
usgs.add_command(search)
usgs.add_command(download_options, "download-options")
usgs.add_command(download_url, "download-url")
