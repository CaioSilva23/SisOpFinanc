import tornado.ioloop
import tornado.web
from apps.user import LoginHandler, RegisterHandler
from apps.acoes import AcaoHandler, AcoesHandler
import tornado.options
# from database.conexao import Conexao


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # auth
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),

            # crud acoes
            (r"/acoes", AcoesHandler),
            (r"/acao/(\d+)", AcaoHandler)
        ]
        settings = dict(
            debug=True,
            cookie_secret='bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',

        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # self.session = Conexao.cria_session()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
