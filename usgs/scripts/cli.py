
import os, json
import click
from usgs import api


def get_node(dataset, node):
    
    if node is None:
        
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(cur_dir, "..", "..", "data")
        dataset_path = os.path.join(data_dir, "datasets.json")
        
        with open(dataset_path, "r") as f:
            datasets = json.loads(f.read())
        
        node = datasets[dataset].upper()
    
    return node


@click.group()
def usgs():
    pass

@click.command()
@click.argument("username")
@click.argument("password")
def login(username, password):
    api_key = api.login(username, password)
    print api_key


@click.command()
def logout():
    print api.logout()


@click.command()
@click.argument("dataset")
@click.argument("scene-ids", nargs=-1)
@click.option("--node", help="The node corresponding to the dataset (CWIC, EE, HDDS, LPVS).", default=None)
@click.option("--api-key", help="API key returned from USGS servers after logging in.", default=None)
def metadata(dataset, scene_ids, node, api_key):
    
    node = get_node(dataset, node)
    
    data = api.metadata(dataset, node, scene_ids, api_key)
    print json.dumps(data)


@click.command()
@click.argument("dataset")
@click.option("--node", help="The node corresponding to the dataset (CWIC, EE, HDDS, LPVS).", default=None)
@click.option("--start-date")
@click.option("--end-date")
@click.option("--longitude")
@click.option("--latitude")
@click.option("--distance", help="Radius - in units of meters - used to search around the specified longitude/latitude.", default=100)
@click.option("--api-key", help="API key returned from USGS servers after logging in.", default=None)
def search(dataset, node, start_date, end_date, longitude, latitude, distance, api_key):
    
    node = get_node(dataset, node)
    
    data = api.search(dataset, node, lat=latitude, lng=longitude, distance=distance, start_date=start_date, end_date=end_date, api_key=api_key)
    print json.dumps(data)


usgs.add_command(login)
usgs.add_command(logout)
usgs.add_command(metadata)
usgs.add_command(search)