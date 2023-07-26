from auth.auth import auth
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
        if (name and description and price_unit and stock):
            try:
                self.save_acao(
                    name=name,
                    description=description,
                    price_unit=price_unit,
                    stock=stock
                )
                return self.write({"message": "Acao created successfully"})
            except Exception:
                pass
        return self.write_error_(msg='Invalid data')


@auth
class AcaoHandler(Base):
    """ações detail"""
    def get(self, id):
        acao = self.acao_get_id(id=id)
        if not acao:
            return self.write_error_(msg='Action not found')
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
        stock_actions = self.list_acoes_for_user()

        if not stock_actions:
            return self.write_error_(msg='Voce não possui ações!')
        else:
            self.write(
                {"My actions":
                    [{"stock_id": stock.id,
                        "action": stock.acao.id,
                        "name": stock.acao.name,
                        "description": stock.acao.description,
                        "quantity": stock.quantity}       
                        for stock in stock_actions]})

    def post(self):
        id = self.data().get('stock_action')
        valor_unit = self.data().get('valor_unit')
        quantity = self.data().get('quantity')

        stock_action = self.stock_action_get(id=int(id))
        if stock_action:
            if stock_action.quantity < quantity:
                return self.write_error_(msg=f"quantidade insuficiente, voce possui {stock_action.quantity}")  # noqa
            save = self.save_operation_sale(
                    quantity=quantity,
                    price_venda=valor_unit,
                    stock_action=stock_action,
                )
            if save:
                return self.write({"success": "ação vendida com sucesso!"})
            else:
                return self.write_error_(msg='error, tente novamente!')
        return self.write_error_(msg='está acão nao possui estoque!')
