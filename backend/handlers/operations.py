from auth.auth import auth
from .base import Base
from logzero import logger


@auth
class OperationsHandler(Base):
    def get(self):
        operations = self.list_operations()
        return self.write({"Operações":
                        [{"id": operation.id,
                            "user_id": self.get_user(),
                            "acao_id": operation.acao_id,
                            "type_operation": operation.type_operation,
                            "status": operation.status,
                            "quantity": operation.quantity,
                            "price_unit": operation.price_unit,
                            "price_total": operation.price_total,
                            "data_operacao": f'{operation.date}'}
                            for operation in operations]})

    def post(self):
        try:
            data = self.data()
            acao_id = int(data.get('acao_id'))
            quantity = int(data.get('quantity'))
        except Exception as e:
            logger.error(e)
            return self.write_error_(msg="dados inválidos")

        user = self.get_detail_user()
        if not (acao_id and quantity):
            return self.write_error_('preencha os campos')

        acao = self.acao_get_id(id=acao_id)
        if not acao:
            return self.write_error_(msg='ação nao encontrada')
        if user.money < float(acao.price_unit) * quantity:
            return self.write_error_(msg=f'Voce não possui fundos suficiente! seu saldo R$ {user.money}')  # noqa
        if acao.stock < quantity:
            return self.write_error_('estoque insuficiente')
        save = self.save_operation_purchase(
            user=user,
            acao=acao,
            quantity=quantity)
        if save:
            self.write({"success": "Compra realizada com sucesso!"})
        else:
            return self.write_error_("error, tente novamente.")


@auth
class OperationHandler(Base):
    def get(self, id):
        operation = self.operation_get_id(id=id)
        if operation:
            return self.write(
                {"Operações":
                    {"id": operation.id,
                     "user_id": self.get_user(),
                      "acao_id": operation.acao_id,
                      "type_operation": operation.type_operation,
                      "quantity": operation.quantity,
                      "price_total": operation.price_total,
                      "data_operacao": f'{operation.date}'}})
        return self.write_error_('Esta operação não é sua ou não existe!')

    def delete(self, id):
        operation = self.operation_get_id(id=id)

        if not operation:
            return self.write_error_(msg="Está operacao não existe.")

        elif operation.status == 'Pendente':
            return self.write_error_(msg="Você só pode deletar transações finalizadas.")  # noqa
        else:
            self.operation_delete(operation)
            return self.write({"success": "operação deletada com successo."})
