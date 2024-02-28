from __future__ import print_function
import json
import traceback
import sys

from dorfaksoftcore.domain.BaseModel import BaseModel
from dorfaksoftcore.infrastructure.JavaScriptSerializer import JavaScriptSerializer


class HashMap(BaseModel):
    values = {}
    def __init__(self):
        self.values = {}

    def to_dict(self):
        return self.values
    def get(self, key):
        if key in self.values:
            return self.values[key]
        else:
            return None
    def put(self, key, value):
        try:
            value=JavaScriptSerializer().toDict(value)
        except  Exception:
            traceback.print_exc()


        self.values[key] = value

    def toString(self):
        return json.dumps(self.values).replace('	',' ').replace('+-.*^%$','\\r\\n')