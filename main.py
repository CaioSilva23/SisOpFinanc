import tornado.ioloop
import tornado.web
from handlers.user import LoginHandler, \
                                    RegisterHandler, \
                                    ChangePasswordHandler,\
                                    UserDetailHandler, \
                                    ResetPasswordHandler
from handlers.acoes import AcaoHandler, AcoesHandler, AcoesForUserHandler
from handlers.operations import OperationsHandler, OperationHandler
import tornado.options
from logzero import logger, logfile, loglevel, INFO


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # auth
            (r"/api/v1/register", RegisterHandler),
            (r"/api/v1/login", LoginHandler),
            (r"/api/v1/change-password", ChangePasswordHandler),
            (r"/api/v1/user", UserDetailHandler),
            (r"/api/v1/reset-password", ResetPasswordHandler),

            # crud acoes
            (r"/api/v1/actions", AcoesHandler),
            (r"/api/v1/action/(\d+)", AcaoHandler),
            (r"/api/v1/actions/user", AcoesForUserHandler),

            # crud operations
            (r"/api/v1/operations", OperationsHandler),
            (r"/api/v1/operation/(\d+)", OperationHandler)
        ]
        settings = dict(
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # self.session = Conexao.cria_session()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8000)

    logger.info(f'Listening server on port {8000}')
    logfile("tornado.log")
    loglevel(INFO)

    tornado.ioloop.IOLoop.instance().start()
