from database.models import Operacao, Acao
from database.conexao import Conexao
from sqlalchemy import func
from queries.query_acao import AcaoQuery


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
    def save(cls, operation, acao_id, tipo_operacao="Compra"):
        if tipo_operacao == "Compra":
            AcaoQuery.update(id=acao_id, quantity=operation.quantity)
            operation = session.add(operation)
            session.commit()
            session.close()

        # elif tipo_operacao == 'Venda':
        #     compra = (
        #     session.query(Operation)
        #         .filter(Operation.user_id == user_id, \
        # Operation.acao_id == acao.id, Operation.type == 'Compra')
        #         .first())

    @classmethod
    def delete(cls, operation):
        session.delete(operation)
        session.commit()
        session.close()

    @classmethod
    def list_acoes(cls, user_id):
        acoes_compradas = (
            session.query(
                Acao,
                func.sum(Operacao.quantity).label('quantity'),
            )
            .join(Operacao)
            .filter(Operacao.user_id == user_id, Operacao.type_operation == 'Compra')  # noqa
            .group_by(Acao)
            .all()
        )

        return acoes_compradas
