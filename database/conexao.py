from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


class Conexao():
    @classmethod
    def conecta(cls):
        db_host = config('db_host', str)
        db_name = config('db_name', str)
        db_user = config('db_user', str)
        db_password = config('db_password', str)
        port = config('port', int)

        CONN = f'postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_name}'  # noqa
        # CONN = "sqlite:///sqlite.db"
        engine = create_engine(CONN, echo=True)
        return engine

    @classmethod
    def cria_session(cls):
        engine = cls.conecta()
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        return session
