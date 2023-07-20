
import tornado.ioloop
import tornado.web
import jwt
import datetime
from tornado.options import define, options
from auth import jwtauth
import os.path

SECRET = 'my_secret_key'

@jwtauth
class MainHandler(tornado.web.RequestHandler):
    """
        Main page handler.
        Needs Authorization to access it
        because here we're using @jwfath decorator
    """
    def get(self, *args, **kwargs):
        self.render('index.html')

class AuthHandler(tornado.web.RequestHandler):
    """
        Handle to auth method.
        This method aim to provide a new authorization token
        There is a fake payload (for tutorial purpose)
    """
    def prepare(self):
        """
            Encode a new token with JSON Web Token (PyJWT)
        """
        self.encoded = jwt.encode({
            'some': 'payload',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)},
            SECRET,
            algorithm='HS256'
        )

    def get(self, *args, **kwargs):
        """
            return the generated token
        """
        response = {'token': self.encoded.decode('ascii')}
        self.write(response)

class Application(tornado.web.Application):
    """
        Application main class
    """
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": True,
        }

        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/auth", AuthHandler, name="auth"),
            tornado.web.url(r"/", MainHandler, name="main"),
        ], **settings)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()