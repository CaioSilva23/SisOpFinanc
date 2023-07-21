import tornado.ioloop
import tornado.web
from database.models import Acao
from handlers.auth import jwtauth, get_user
from database.query_acao import acoes_list, get_acao_id
import json


@jwtauth
class AcoesHandler(tornado.web.RequestHandler):
    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    async def get(self):
        acoes = acoes_list(user_id=get_user(self.get_token()))
        self.write({"Ações": [{"id": acao.id,
                               "name": acao.name,
                               "description": acao.description,
                               "value": acao.value,
                               "user_id": acao.user_id} for acao in acoes]})  # noqa

    async def post(self):
        data = self.request.body
        json_data = json.loads(data)
        name = json_data.get('name')
        description = json_data.get('description')
        value = json_data.get('value')
        acao = Acao(name=name, description=description,value=value, user_id=self.get_user_id())  # noqa
        self.application.session.add(acao)
        self.application.session.commit()
        self.write({"message": "Acao created successfully"})


@jwtauth
class AcaoHandler(tornado.web.RequestHandler):
    # SUPPORTED_METHODS = ("GET", "PUT", "DELETE")

    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    async def get(self, id):
        user_id = get_user(token=self.get_token())
        acao = get_acao_id(user_id=user_id, id=id)
        if not acao:
            self.set_status(404)
            return self.write({'error': {'acao': 'Ação not found'}})
        return self.write({"Ação": {"id": acao.id, "name": acao.name, "description": acao.description, "value": acao.value, "user": acao.user_id}})  # noqa
