from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Conexao():

    @classmethod
    def conecta(cls):

        # USUARIO = 'root'
        # SENHA = '1234'
        # HOST = 'localhost'
        # BANCO = 'fastapi'
        # PORT = '3306'
        # CONN = f'mysql://{USUARIO}:{SENHA}@{HOST}:{PORT}/{BANCO}'
        # sqlite:///:dbsqlite
        # CONN = f'sqlite:///:dbsqliteteste'
        engine = create_engine("sqlite:///sqlite.db", echo=True)

        return engine

    @classmethod
    def cria_session(cls):
        conexao = cls.conecta()
        Session = sessionmaker(bind=conexao)
        session = Session()
        return session
