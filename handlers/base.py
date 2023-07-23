import tornado.ioloop
import tornado.web
import json
from json import JSONDecodeError
from handlers.auth import get_user


class Base(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        # HEADERS!
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    def data(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError:
            return {}

    def get_user(self):
        return get_user(token=self.get_token())
