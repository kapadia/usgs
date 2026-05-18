
import os
import json

import requests

testdir = os.path.dirname(os.path.abspath(__file__))


class MockPost(object):


    def __init__(self, filename=None, status_code=200, reason="OK"):
        self.filename = filename
        self.status_code = status_code
        self.reason = reason


    def __call__(self, url, payload=None):
        return self


    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(
                "%d %s" % (self.status_code, self.reason))
        return None


    def json(self):
        filepath = os.path.join(testdir, 'data', self.filename)

        with open(filepath) as f:
            data = json.load(f)

        return data