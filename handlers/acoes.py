from auth.auth import auth
from .base import Base
from logzero import logger


@auth
class AcoesHandler(Base):
    def get(self):
        acoes = self.acoes_list()
        if acoes:
            return self.write(
                {"Ações":
                    [{"id": acao.id,
                      "name": acao.name,
                      "description": acao.description,
                      "price_unit": acao.price_unit,
                      "stock": acao.stock,
                      "oferta": True if acao.oferta else False}
                        for acao in acoes]})
        return self.write({"info": "Nenhuma ação disponível a venda!"})

    def post(self):
        try:
            data = self.data()
            name = data.get('name')
            description = data.get('description')
            price_unit = float(data.get('price_unit'))
            stock = int(data.get('stock'))
        except Exception as e:
            logger.error(e)
            return self.write_error_(msg="Dados inválidos.")

        if (name and description and price_unit and stock):
            self.save_acao(
                name=name,
                description=description,
                price_unit=price_unit,
                stock=stock
                )
            return self.write({"success": "Ação criada com sucesso."})
        return self.write_error_(msg='Dados inválidos.')


@auth
class AcaoHandler(Base):
    def get(self, id):
        acao = self.acao_get_id(id=id)
        if acao:
            return self.write(
                {"id": acao.id,
                    "name": acao.name,
                    "description": acao.description,
                    "price_unit": acao.price_unit,
                    "stock": acao.stock,
                    "oferta": True if acao.oferta else False})
        return self.write_error_(msg='Ação não encontrada')


@auth
class AcoesForUserHandler(Base):
    def get(self):
        stock_actions = self.list_acoes_for_user()

        if not stock_actions:
            return self.write_error_(msg='Voce não possui ações!')
        else:
            self.write(
                {"acoes":
                    [{"stock_id": stock.id,
                        "action": stock.acao.id,
                        "name": stock.acao.name,
                        "description": stock.acao.description,
                        "quantity": stock.quantity} 
                        for stock in stock_actions]})

    def post(self):
        try:
            id = self.data().get('stock_action')
            valor_unit = float(self.data().get('valor_unit'))
            quantity = int(self.data().get('quantity'))
        except Exception as e:
            logger.error(e)
            return self.write_error_(msg="dados inválidos!")

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
