from handlers.auth import auth
from .base import Base


@auth
class OperationsHandler(Base):
    def get(self):
        """lista minhas operações"""
        operations = self.list_operations()
        self.write({"Operações":
                    [{"id": operation.id,
                      "user_id": self.get_user(),
                      "acao_id": operation.acao_id,
                      "type_operation": operation.type_operation,
                      "quantity": operation.quantity,
                      "price_total": operation.price_total,
                      "data_operacao": f'{operation.date}'}
                        for operation in operations]})

    def post(self):
        """operacao de compra"""
        data = self.data()
        acao_id = data.get('acao_id')
        quantity = data.get('quantity')
        user = self.get_detail_user()

        if not (acao_id and quantity):
            return self.write({"error": "preencha os campos"})

        acao = self.acao_get_id(id=acao_id)
        if not acao:
            return self.write({"error": "ação nao encontrada"})
        if user.money < acao.price_unit * quantity:
            return self.write({"error": "voce não possui fundos suficiente!"})
        if acao.stock < quantity:
            return self.write({"error": "estoque insuficiente"})
        save = self.save_operation_purchase(
            user=user,
            acao=acao,
            quantity=quantity)
        if save:
            return self.write({"message": "Operation created successfully"})
        else:
            return self.write({"error": "error, tente novamente!"})


@auth
class OperationHandler(Base):
    """detail operation for user"""
    def get(self, id):
        operation = self.operation_get_id(id=id)
        if operation:
            return self.write({"Operações":
                    {"id": operation.id,
                      "user_id": self.get_user(),
                      "acao_id": operation.acao_id,
                      "type_operation": operation.type_operation,
                      "quantity": operation.quantity,
                      "price_total": operation.price_total,
                      "data_operacao": f'{operation.date}'}
                        })
        return self.write({"error": "Esta operação não é sua ou não existe!"})
