from database.models import Acao
from handlers.auth import jwtauth
from queries.query_acao import AcaoQuery
from .base import Base


@jwtauth
class AcoesHandler(Base):
    def get(self):
        acoes = AcaoQuery.list()
        if not acoes:
            return self.write({"info": "nenhuma ação disponível a venda!"})
        self.write({"Ações":
                    [{"id": acao.id, "name": acao.name,
                        "description": acao.description,
                        "price_unit": acao.price_unit,
                        "stock": acao.stock}
                        for acao in acoes]})  # noqa

    def post(self):
        data = self.data()

        name = data.get('name')
        description = data.get('description')
        price_unit = data.get('price_unit')
        stock = data.get('stock')

        nova_acao = Acao(name=name,
                         description=description,
                         price_unit=price_unit,
                         stock=stock)

        AcaoQuery.save(acao=nova_acao)
        self.write({"message": "Acao created successfully"})


class AcaoHandler(Base):
    def get(self, id):
        acao = AcaoQuery.get_id(id=id)
        if not acao:
            self.set_status(404)
            return self.write({'error': {'acao': 'Ação not found'}})
        return self.write({"Ação":
                           {"id": acao.id,
                            "name": acao.name,
                            "description": acao.description,
                            "price_unit": acao.price_unit,
                            "stock": acao.stock
                            }})
