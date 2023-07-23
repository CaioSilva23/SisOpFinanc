from database.models import Operacao
from handlers.auth import jwtauth
from queries.query_acao import AcaoQuery
from queries.operation_query import OperationQuery
from .base import Base
import datetime


@jwtauth
class OperationsHandler(Base):
    def get(self):
        operations = OperationQuery.list(user_id=self.get_user())
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
        data = self.data()

        acao_id = data.get('acao_id')
        type_operation = data.get('type_operation')
        quantity = data.get('quantity')

        if not (acao_id and type_operation and quantity):
            return self.write({"error": "preencha os campos"})

        acao = AcaoQuery.get_id(id=acao_id)

        if not acao:
            return self.write({"error": "ação nao encontrada"})

        if ('Compra' or 'Venda') not in type_operation:
            return self.write({"Error": "Tipo de operação inválida!"})

        if acao.stock < quantity:
            return self.write({"error": "estoque insuficiente"})

        date = datetime.datetime.now()

        nova_operacao = Operacao(
            user_id=self.get_user(),
            acao_id=acao_id,
            type_operation=type_operation,
            quantity=quantity,
            price_total=acao.price_unit * quantity,
            date=date
            )

        OperationQuery.save(operation=nova_operacao, acao_id=acao_id)
        self.write({"message": "Operation created successfully"})


@jwtauth
class OperationHandler(Base):
    def get(self):
        minhas_acoes = OperationQuery.list_acoes(user_id=self.get_user())

        if not minhas_acoes:
            return self.write({"Ações": "Voce não possui ações!"})
        return self.write(
            {"Suas ações":
                [{"id": acao.id,
                    "name": acao.name,
                    "description": acao.description,
                    "quantity": quantity
                  }
                    for acao, quantity in minhas_acoes]}
                    )


class OperationIdHandler(Base):
    def delete(self, id):
        operation = OperationQuery.get_id(id=id)
        if operation:
            OperationQuery.delete(operation=operation)
            return self.write({"success": "Operação deletada com sucesso!"})
        else:
            return self.write({"error": "Esta operação não existe!"})

