from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Conexao:
    @classmethod
    def conecta(cls):

        user = 'caio'
        password = 'Caua2023'
        host = 'localhost'
        db = 'tornado_project'
        port = 5432
        DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        # sqlite:///:dbsqlite
        # CONN = f'sqlite:///:dbsqliteteste'
        engine = create_engine(DATABASE_URI, echo=True)

        return engine

    @classmethod
    def cria_session(cls):
        conexao = cls.conecta()
        Session = sessionmaker(bind=conexao)
        session = Session()
        return session
