
import os
import json

testdir = os.path.dirname(os.path.abspath(__file__))


class MockPost(object):


    def __init__(self, filename):
        self.filename = filename


    def __call__(self, url, payload):
        return self


    def json(self):
        filepath = os.path.join(testdir, 'data', self.filename)

        with open(filepath) as f:
            data = json.load(f)

        return data