from database.models import Acao
from handlers.auth import jwtauth, get_user
from queries.query_acao import AcaoQuery
from .base import AcaoBase


@jwtauth
class AcoesHandler(AcaoBase):
    async def get(self):
        acoes = await AcaoQuery.list(user_id=get_user(token=self.get_token()))
        self.write({"Ações": [{"id": acao.id,
                               "name": acao.name,
                               "description": acao.description,
                               "value": acao.value,
                               "user_id": acao.user_id} for acao in acoes]})  # noqa

    async def post(self):
        data = self.data()

        name = data.get('name')
        description = data.get('description')
        value = data.get('value')

        nova_acao = Acao(name=name,
                         description=description,
                         value=value,
                         user_id=get_user(token=self.get_token()))  

        AcaoQuery.save(acao=nova_acao)
        self.write({"message": "Acao created successfully"})


@jwtauth
class AcaoHandler(AcaoBase):
    async def get(self, id):
        user_id = get_user(token=self.get_token())
        acao = AcaoQuery.get_id(user_id=user_id, id=id)
        if not acao:
            self.set_status(404)
            return self.write({'error': {'acao': 'Ação not found'}})
        return self.write({"Ação":
                           {"id": acao.id,
                            "name": acao.name,
                            "description": acao.description,
                            "value": acao.value,
                            "user": acao.user_id}})
