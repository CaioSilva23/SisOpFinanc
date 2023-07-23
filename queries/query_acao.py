from database.models import Acao
from database.conexao import Conexao


session = Conexao.cria_session()


class AcaoQuery:
    @classmethod
    def list(cls):
        acoes = session.query(Acao).filter(Acao.stock > 0).all()
        return acoes

    @classmethod
    def get_id(cls, id):
        acao = session.query(Acao).filter_by(id=id).first()
        return acao

    @classmethod
    def save(self, acao):
        acao = session.add(acao)
        session.commit()
        session.close
        return acao

    @classmethod
    def update(cls, id, quantity=None):
        acao = cls.get_id(id=id)
        acao.stock -= quantity
        session.commit()
        session.close()
