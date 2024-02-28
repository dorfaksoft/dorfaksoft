from flask import url_for


class RequestHelper():
    @staticmethod
    def getIp(req=None):
        if not req:
            from flask import request
            req = request

        return req.headers.get('X-Forwarded-For', req.remote_addr)

    @staticmethod
    def getRefererUrl(req=None):
        if not req:
            from flask import request
            req = request
        return req.headers.get("Referer") or req.args.get('next') or req.referrer
