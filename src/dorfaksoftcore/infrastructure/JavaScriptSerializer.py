import json
import ast

from dorfaksoftcore.domain.BaseModel import BaseModel


class JavaScriptSerializer():
    def serialize(self, data):
        from dorfaksoftcore.domain.Entity import Entity
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], Entity):
            return json.dumps([ast.literal_eval(ob.toString()) for ob in data]).replace('+-.*^%$', '\r\n')
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], BaseModel):
            return json.dumps([ob.get_compact_dict() for ob in data]).replace("'",'"')
        elif isinstance(data, Entity):
            return data.toString().replace('+-.*^%$', '\\r\\n')
        elif isinstance(data, BaseModel):
            return str(data)
        else:
            return json.dumps(data)

    def toDict(self, data):

        from dorfaksoftcore.domain.Entity import Entity
        if isinstance(data, list):
            st = JavaScriptSerializer().serialize(data)
        elif isinstance(data, Entity):
            st = data.toString()
        elif isinstance(data, BaseModel):
            st = str(data)
        else:
            return data
        return ast.literal_eval(st.replace(': null', ': ""').replace('\r\n', '+-.*^%$'))
