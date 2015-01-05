
import os, json
import click
import usgs


@click.group()
def usgs():
    pass


@click.command()
@click.argument("dataset")
@click.argument("scene-ids", nargs=-1)
@click.option("--node")
@click.option("--api-key")
def metadata(dataset, scene_ids, node, api_key=None):
    
    from usgs import api
    
    if node is None:
        
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        data_dir = os.path.join(cur_dir, "..", "..", "data")
        dataset_path = os.path.join(data_dir, "datasets.json")
        
        with open(dataset_path, "r") as f:
            datasets = json.loads(f.read())
        
        node = datasets[dataset].upper()
    
    data = api.metadata(dataset, node, scene_ids, api_key)
    print json.dumps(data)


# @click.command()
# @click.option("--start-date")
# @click.option("--end-date")
# @click.option("--longitude")
# @click.option("--latitude")
# @click.option("--dataset", default="LANDSAT_8")
# @click.option('--output', help="Output a JSON file containing metadata", default=None)
# def search(start_date, end_date, longitude, latitude, dataset, output):
#     import csv, json
#
#     from mapbox.usgs.authentication import login, logout
#     from mapbox.usgs.search import get_scenes
#
#     api_key = login()
#     scenes = get_scenes(
#         start_date=start_date,
#         end_date=end_date,
#         longitude=longitude,
#         latitude=latitude,
#         dataset=dataset,
#         api_key=api_key)
#
#     if output:
#         with open(output, "w") as dst:
#             dst.write(json.dumps(scenes))
#
#     scene_ids = map(lambda d: d["entityId"], scenes)
#
#     for scene_id in scene_ids:
#         print scene_id


# usgs.add_command(search)
usgs.add_command(metadata)