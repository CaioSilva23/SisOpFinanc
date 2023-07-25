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
        type_operation = data.get('type_operation')
        quantity = data.get('quantity')

        if not (acao_id and type_operation and quantity):
            return self.write({"error": "preencha os campos"})

        if ('Compra' or 'Venda') not in type_operation:
            return self.write({"Error": "Tipo de operação inválida!"})

        if type_operation == 'Compra':
            acao = self.acao_get_id(id=acao_id)
            if not acao:
                return self.write({"error": "ação nao encontrada"})
            if acao.stock < quantity:
                return self.write({"error": "estoque insuficiente"})
            self.save_operation(
                acao_id=acao_id,
                type_operation=type_operation,
                quantity=quantity)
            return self.write({"message": "Operation created successfully"})
        elif type_operation == 'Venda':
            return


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
