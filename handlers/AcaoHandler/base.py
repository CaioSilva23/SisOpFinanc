import tornado.ioloop
import tornado.web
import json
from json import JSONDecodeError


class AcaoBase(tornado.web.RequestHandler):
    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    def data(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError:
            return {}