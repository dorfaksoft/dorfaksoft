# coding=utf-8
import decimal
import json
import re
from datetime import datetime

from dorfaksoftcore.domain.HashMap import HashMap
from dorfaksoftcore.infrastructure.JavaScriptSerializer import JavaScriptSerializer


class Entity:
    JSON_ALIAS = {}
    brokenRule = None
    error = ''

    def __iter__(self):
        for attr, value in self.__dict__.items():
            if attr.lower() == "json_alias" or attr.lower() == "jsonalias":
                yield "", ""
            elif isinstance(value, datetime):
                iso = value.isoformat()
                yield self.getAlias(attr), iso
            elif isinstance(value, decimal.Decimal):
                yield self.getAlias(attr), str(value)
            elif isinstance(value, list):
                yield self.getAlias(attr), JavaScriptSerializer().toDict(value)
            elif isinstance(value, str):
                yield self.getAlias(attr), value.replace('"', '').replace('\r\n', '+-.*^%$').replace('\n', '+-.*^%$')
            elif hasattr(value, '__iter__'):
                if hasattr(value, 'pop'):
                    yield self.getAlias(attr), value
                else:
                    yield self.getAlias(attr), dict(value)
            elif isinstance(value, HashMap):
                yield self.getAlias(attr), value.values
            elif value is None:
                yield "", ""
            else:
                yield self.getAlias(attr), value

    def setBrokenRule(self, brokenRule):
        self.brokenRule = brokenRule

    def getBrokenRule(self):
        return self.brokenRule

    def setError(self, error):
        self.error = error

    def getError(self):
        return self.error

    def hasError(self):
        return self.brokenRule != None or self.error != ''

    def getAlias(self, attr):
        return (self.JSON_ALIAS[attr] if attr in self.JSON_ALIAS else attr)

    def model_binding(self, valid_fields=None, is_none=True, dictionary=None,isCamel=False):
        if not dictionary:
            from flask import request
            dictionary = request.form.to_dict()
        if not dictionary:
            from flask import request
            dictionary = request.json
        for k, v in dictionary.items():
            if isCamel:
                components = k.split('_')
                k = components[0] + ''.join(x.title() for x in components[1:])
            else:
                k = re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower()
            if not valid_fields or k in valid_fields:
                if is_none:
                    setattr(self, k, v or None)
                else:
                    setattr(self, k, v)
        return self

    def get_camel_dict(self):
        dictionary = self.__dict__
        res = {}
        for k, v in dictionary.items():
            if v is None:
                continue
            components = k.split('_')
            k = components[0] + ''.join(x.title() for x in components[1:])
            res[k] = v
        if "JSONAlias" in res:
            del res["JSONAlias"]
        return res

    def get_snake_dict(self):
        dictionary = self.__dict__
        res = {}
        for k, v in dictionary.items():
            if v is None:
                continue
            res[k] = v
        return res

    def bindField(self, dictionary, camel_case=True):
        for k, v in dictionary.items():
            if camel_case and k.find('_') != -1:
                components = k.split('_')
                k = components[0] + ''.join(x.title() for x in components[1:])
            setattr(self, k, v)
        return self

    def toString(self, with_enter=False):
        res = json.dumps(dict(self)).strip()
        if with_enter:
            res = res.replace('+-.*^%$', "\r\n")

        return res
