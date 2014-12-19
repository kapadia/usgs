
import os
import sys
import re
import subprocess
from urlparse import parse_qs
import requests
from bs4 import BeautifulSoup
from boto.s3.connection import S3Connection

from mapbox.usgs.authentication import login
from mapbox.usgs import authentication, USGSApiKeyRequiredError, EARTH_EXPLORER_CATALOG_NODE
from mapbox.usgs.xml_requests import download_request


def get_usgs_download_urls(scene_ids, api_key=None):
    """
    Query the USGS Inventory Service authorized data URLs.
    """
    retries = 5
    
    if api_key is None:
        api_key = login()
    
    params = {
        "dataset": "LANDSAT_8",
        "node": EARTH_EXPLORER_CATALOG_NODE,
        "api_key": api_key,
        "product": "STANDARD"
    }
    
    xml_request = download_request % params
    
    bs = BeautifulSoup(xml_request, "xml")
    entityIds = bs.find("entityIds")
    
    for scene_id in scene_ids:
        scene_id_item = BeautifulSoup('<item xsi:type="xsd:string">%s</item>' % scene_id, "html.parser")
        entityIds.append(scene_id_item)
    
    for attempt in range(retries, 0, -1):
        if attempt != retries:
            time.sleep(10)
        try:
            resp = requests.post("https://earthexplorer.usgs.gov/inventory/soap", str(bs))
            break
        except:
            pass
    
    xml_data = BeautifulSoup(resp.text)
    
    items = xml_data.findAll('item')
    return map(lambda d: d.text, items)


def download_from_usgs(url, dstpath, attempt=0):
    """
    Download a file from USGS. This is here for convenience, and it
    might be more practical to use `get_usgs_download_urls` followed by a parallel curl.
    """
    if attempt == 3:
        sys.exit(1)
    
    if not dstpath:
        dstpath = os.path.basename(url).split("?")[0]
    
    dstpath = dstpath.replace("tar.bz", "tar.gz")
    
    # Remove query string if present
    dstpath = dstpath.split("?")[0]
    
    url = url.replace('\\', '')
    base_url, qs = url.split("?")
    qs = parse_qs(qs)
    
    print "Requesting %s" % os.path.basename(base_url)
    print base_url
    params = {'did': qs['did'][0], 'iid': qs['iid'][0]}
    r = requests.get(base_url, params=params, stream=True)
    
    if r.status_code != 200:
        scene_id = params['iid']
        url = get_usgs_download_urls([scene_id])[0]
        attempt += 1
        download_from_usgs(url, dstpath, attempt=attempt)
    
    if not dict(r.headers).has_key('content-length'):
        sys.exit(1)
    
    length = float(r.headers.get('content-length'))
    
    bytes_received = 0.0
    
    with open(dstpath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                bytes_received += len(chunk)
                percent_received = 100.0 * bytes_received / length
                chunks_received = int(50 * bytes_received / length)
                
                sys.stdout.write("\r[%s%s] %.2f%%" % ('#' * chunks_received, ' ' * (50 - chunks_received), percent_received))
                sys.stdout.flush()
                f.write(chunk)
                f.flush()
    
    return dstpath


def download_from_s3(sceneid, dstpath):
    """
    Given a Landsat scene id, attempt to download the scene from 
    the Mapbox stash. This function assumes that files are stored
    under a specific URL.
    
    LC82331222014329LGN00.tar.gz
    s3://mapbox-cloudless-testing/landsat8/scenes/[path]/[row]/[year][julian doy]/[scene_id].tif
    
    :param sceneid:
        The Landsat 8 scene id.
    
    :param dstpath:
        The destination file path for the downloaded object.
    """
    match = re.search("^(LC8|LT8)(?P<path>\d{3})(?P<row>\d{3})(?P<year>\d{4})(?P<doy>\d{3})[A-Z]{3}\d{2}$", sceneid)
    
    params = { "sceneid": sceneid }
    params.update(match.groupdict())
    keypath = "landsat8/scenes/%(path)s/%(row)s/%(year)s%(doy)s/%(sceneid)s.tar.gz" % params
    dstpath = dstpath.replace("tar.bz", "tar.gz")
    
    aws_connection = S3Connection()
    bucket = aws_connection.get_bucket('mapbox-cloudless-testing')
    key = bucket.get_key(keypath)
    
    if key is None:
        return False
    
    key.get_contents_to_filename(dstpath)
    return True


def download_from_google(sceneid, dstpath):
    """
    Download a Landsat 8 scene from Google Earth Engine.
    """
    match = re.search("^(LC8|LT8)(?P<path>\d{3})(?P<row>\d{3})(?P<year>\d{4})(?P<doy>\d{3})[A-Z]{3}\d{2}$", sceneid)
    params = { "sceneid": sceneid }
    params.update(match.groupdict())
    
    keypath = "gs://earthengine-public/landsat/L8/%(path)s/%(row)s/%(sceneid)s.tar.bz" % params
    dstpath = dstpath.replace("tar.gz", "tar.bz")
    
    if subprocess.call(["gsutil", "cp", keypath, dstpath]) == 0:
        return True
    
    return False
    