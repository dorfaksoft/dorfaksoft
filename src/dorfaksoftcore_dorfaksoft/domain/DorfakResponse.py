# coding=utf-8
from flask import make_response

from dorfaksoftcore.domain.Entity import Entity


class DorfakResponse(Entity):
    JSON_ALIAS = {"data": "d", "success": "s", "brokenRule": "e", "error": "r","data2":"d2","message":"m"}

    data = ''
    data2 = ''
    message = ''
    success = False
    error = ''

    brokenRule = None

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getData2(self):
        return self.data2

    def setData2(self, data2):
        self.data2 = data2

    def getMessage(self):
        return self.message

    def setMessage(self, message):
        self.message = message

    def getSuccess(self):
        return self.success

    def setSuccess(self, success):
        self.success = success

    def setBrokenRule(self, brokenRule):
        self.brokenRule = brokenRule

    def setError(self, error):
        self.error = error

    def makeResponse(self):
        response = make_response(self.toString())
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response
