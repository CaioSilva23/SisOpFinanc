import tornado.ioloop
import tornado.web
import json
from json import JSONDecodeError


class UserBase(tornado.web.RequestHandler):
    def data(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError:
            return {}
