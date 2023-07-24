from handlers.auth import jwtauth
from .base import Base


@jwtauth
class AcoesHandler(Base):
    """list acoes disponíveis"""
    def get(self):
        acoes = self.acoes_list()
        if acoes:
            return self.write({"Ações":
                    [{"id": acao.id, "name": acao.name,
                        "description": acao.description,
                        "price_unit": acao.price_unit,
                        "stock": acao.stock}
                        for acao in acoes]})
        return self.write({"info": "nenhuma ação disponível a venda!"})

    def post(self):
        """post ação"""
        data = self.data()

        name = data.get('name')
        description = data.get('description')
        price_unit = data.get('price_unit')
        stock = data.get('stock')

        try:
            self.save_acao(
                name=name,
                description=description,
                price_unit=price_unit,
                stock=stock
            )
            self.write({"message": "Acao created successfully"})
        except Exception:
            self.write({"error": "error ao salvar a ação "})


class AcaoHandler(Base):
    """ações detail"""
    def get(self, id):
        acao = self.acao_get_id(id=id)
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


@jwtauth
class AcoesForUserHandler(Base):
    def get(self):
        minhas_acoes = self.list_acoes_for_user()

        if not minhas_acoes:
            return self.write({"Ações": "Voce não possui ações!"})
        return self.write(
            {"Suas ações":
                [{"name": acao.name,
                    "description": acao.description,
                    "quantity": quantity
                  }
                    for acao, quantity in minhas_acoes]}
                    )
