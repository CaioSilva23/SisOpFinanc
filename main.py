import tornado.ioloop
import tornado.web
from dao_user import UsersHandler, LoginHandler


def make_app():
    return tornado.web.Application([
        (r"/users", UsersHandler),
        (r"/login", LoginHandler)
        # (r"/auth", AuthHandler,),
        # (r"/users/(\d+)", UserHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
