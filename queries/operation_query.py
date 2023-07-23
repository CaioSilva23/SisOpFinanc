from database.models import Operacao, Acao
from database.conexao import Conexao
from sqlalchemy import func


session = Conexao.cria_session()


class OperationQuery:
    @classmethod
    def list(cls, user_id):
        operations = session.query(Operacao).filter_by(user_id=user_id)
        return operations

    @classmethod
    def get_id(cls, id):
        operation = session.query(Operacao).filter_by(id=id).first()
        return operation

    @classmethod
    def save(cls, operation, acao, tipo_operacao="Compra"):
        if tipo_operacao == "Compra":
            acao.stock -= operation.quantity
            operation = session.add(operation)
            session.commit()
            session.close()
        # elif tipo_operacao == 'Venda':
        #     compra = (
        #     session.query(Operation)
        #         .filter(Operation.user_id == user_id, Operation.acao_id == acao.id, Operation.type == 'Compra')
        #         .first())
        return operation

    @classmethod
    def delete(cls, operation):
        session.delete(operation)
        session.commit()
        session.close()

    @classmethod
    def get_id(cls, id):
        operation = session.query(Operacao).filter_by(id=id).first()
        return operation

    @classmethod
    def list_acoes(cls, user_id):
        acoes_compradas = (
            session.query(
                Acao,
                func.sum(Operacao.quantity).label('quantity'),
            )
            .join(Operacao)
            .filter(Operacao.user_id == user_id, Operacao.type_operation == 'Compra')
            .group_by(Acao)
            .all()
        )

        return acoes_compradas

    @classmethod
    def get_operation_and_acao(cls, acao_id):
        operation = session.query(Operacao).filter_by(acao_id=acao_id).first()
        return operation

    @classmethod
    def update_operacao_acao(cls, operacao, nova_operacao):
        operacao.quantity += nova_operacao.quantity
        operacao.price_total = operacao.quantity * nova_operacao.price_unit
        session.commit()
        session.close()
