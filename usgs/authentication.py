
import os
import time
import requests
import dotenv
from bs4 import BeautifulSoup

from mapbox.usgs import endpoint
from mapbox.usgs.xml_requests import login_request, logout_request


module_path = os.path.join(os.path.dirname(__file__), '..', '..')
credentials_path = os.path.join(module_path, ".env")

if os.path.exists(credentials_path):
    dotenv.load_dotenv(credentials_path)
else:
    dotenv.flatten_and_write(credentials_path, {})


def login():
    retries = 5
    api_key = None
    
    credentials = {
        "username": os.environ['USGS_USERNAME'],
        "password": os.environ['USGS_PASSWORD']
    }
    
    for attempt in range(retries+1):
        try:
            r = requests.post(endpoint, login_request % credentials)
            response = BeautifulSoup(r.text, "xml")
            node = response.find('return')
            api_key = node.text
            break
        except:
            pass
        time.sleep(2**attempt)
    
    return api_key


def save_new_login():
    newlogin = login()
    print "Got a new login: %s" % (newlogin)
    dotenv.set_key(credentials_path, 'USGS_API_KEY', newlogin)
    return newlogin


def get_old_login():
    # These semantics are probably broken. We should
    # better distinguish the possible cases:
    # 1. A good login exists in .env
    # 2. An exired login exists in .env
    # 3. No logins are set
    try:
        return os.environ['USGS_API_KEY']
    except:
        print "There was no old login; generating a new one."
        return save_new_login()


def logout(api_key):
    
    r = requests.post(endpoint, logout_request % {"api_key": api_key})
    if not r.status_code == 200:
        raise RuntimeError("USGS logout failed")
    
    return True

