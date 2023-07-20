import tornado.ioloop
import tornado.web
from apps.user import LoginHandler, RegisterHandler
from apps.acoes import AcaoHandler, AcoesHandler
import tornado.options
#import torndb
from tornado.options import options


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),
            (r"/acoes", AcoesHandler),
            (r"/acao/(\d+)", AcaoHandler)
        ]
        settings = dict(
            debug=True,
            cookie_secret='bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',

        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # self.db = torndb.Connection(
        #     host = options.mysql_host,
        #     database = options.mysql_database,
        #     user = options.mysql_user,
        #     password = options.mysql_password,)
        


# def make_app():
#     return tornado.web.Application([
#         (r"/register", RegisterHandler),
#         (r"/login", LoginHandler),
#         (r"/acoes", AcoesHandler),
#         (r"/acao/(\d+)", AcaoHandler)
#         # (r"/auth", AuthHandler,),
#         # (r"/users/(\d+)", UserHandler),
#     ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()
