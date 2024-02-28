# coding=utf-8
import re
from datetime import datetime, timedelta, date
from enum import Enum
from uuid import UUID


class BaseModel:
    error = ''

    def has_error(self):
        return self.error is not None and self.error != ''

    def hasError(self):
        return self.error is not None and self.error != ''

    def setError(self, error):
        self.error = error

    def set_error(self, error):
        self.error = error

    def get_error(self):
        return self.error

    def getError(self):
        return self.error

    def to_dict(self):
        return {}

    def get_compact_dict(self):
        dct = self.to_dict()
        return BaseModel.normalize_dict(dct)

    def model_binding(self, valid_fields=None, is_none=True, dictionary=None,is_camel=True):
        from flask import request
        if not dictionary:
            dictionary = request.form.to_dict()
        if not dictionary:
            dictionary = request.json
        if not dictionary:
            return self
        for k, v in dictionary.items():
            if is_camel:
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
            if not isinstance(v, Enum):
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

    def __repr__(self):
        return str(self.get_compact_dict()).replace("'", "\"").replace("\\xa0", " ")

    @staticmethod
    def normalize_dict(dct):

        for attr, value in dct.copy().items():
            if value is None:
                del dct[attr]
            elif isinstance(value, datetime):
                iso = value.isoformat()
                dct[attr] = iso
            elif isinstance(value, timedelta):
                dct[attr] = str(value)
            elif isinstance(value, date):
                dct[attr] = str(value)
            elif isinstance(value, UUID):
                dct[attr] = value.hex
        return dct
