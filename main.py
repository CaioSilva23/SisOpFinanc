import tornado.ioloop
import tornado.web
from handlers.user import LoginHandler, \
                                    RegisterHandler, \
                                    ChangePasswordHandler
from handlers.acoes import AcaoHandler, AcoesHandler
from handlers.operations import OperationsHandler, OperationHandler, OperationIdHandler
import tornado.options
from logzero import logger


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # auth
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),
            (r"/change-password", ChangePasswordHandler),
            # (r"/reset-password", ResetPassword),

            # crud acoes
            (r"/acoes", AcoesHandler),
            (r"/acao/(\d+)", AcaoHandler),

            # crud operations
            (r"/operations", OperationsHandler),
            (r"/operation", OperationHandler),
            (r"/operation/(\d+)", OperationIdHandler)
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
    logger.info(f'Listening server on port {8888}')
    tornado.ioloop.IOLoop.instance().start()
