from database.models import Acao
from database.conexao import Conexao


session = Conexao.cria_session()


def acoes_list(user_id):
    acoes = session.query(Acao).filter_by(user_id=user_id)
    return acoes


def get_acao_id(user_id, id):
    acao = session.query(Acao).filter_by(user_id=user_id, id=id).first()
    return acao
