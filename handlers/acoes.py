from handlers.auth import auth
from .base import Base

@auth
class AcoesHandler(Base):
    """list acoes disponíveis"""
    def get(self):
        acoes = self.acoes_list()
        if acoes:
            return self.write({"Ações":
                    [{"id": acao.id,
                      "name": acao.name,
                      "description": acao.description,
                      "price_unit": acao.price_unit,
                      "stock": acao.stock,
                      "oferta": True if acao.oferta else False}
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
        except Exception as e:
            self.write({"error": f"error ao salvar a ação {e}"})


@auth
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
                            "stock": acao.stock,
                            "oferta": True if acao.oferta else False
                            }})


@auth
class AcoesForUserHandler(Base):
    def get(self):
        minhas_acoes = self.list_acoes_for_user()

        if not minhas_acoes:
            return self.write({"Ações": "Voce não possui ações!"})
        return self.write(
            {"Suas ações":
                [{"operation": operacoes.id,
                    "date": f'{operacoes.date}',
                    "name": operacoes.acao.name,
                    "description": operacoes.acao.description,
                    "quantity": operacoes.quantity,
                    "value": operacoes.price_total
                  }
                    for operacoes in minhas_acoes]}
                    )

    def post(self):
        id = self.data().get('operacao')
        valor_unit = self.data().get('valor_unit')
        quantidade = self.data().get('quantity')

        operacao = self.operation_get_id(id=int(id))

        if operacao.quantity < quantidade:
            return self.write({"error": f"quantidade insuficiente, voce possui {operacao.quantity}"})  # noqa

        save = self.save_operation_sale(
                quantity=quantidade,
                price_venda=valor_unit,
                old_operation=operacao,
               )
        if save:
            return self.write({"success": "ação vendida com sucesso!"})
        else:
            return self.write({"error": "error, tente novamente!"})