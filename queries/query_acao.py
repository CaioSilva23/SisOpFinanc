from database.models import Acao
from database.conexao import Conexao


session = Conexao.cria_session()


class AcaoQuery:
    @classmethod
    async def list(cls, user_id):
        acoes = session.query(Acao).filter_by(user_id=user_id)
        return acoes

    @classmethod
    def get_id(cls, user_id, id):
        acao = session.query(Acao).filter_by(user_id=user_id, id=id).first()
        return acao

    @classmethod
    def save(self, acao):
        acao = session.add(acao)
        session.commit()
        session.close
        return acao
