from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config


class Conexao():
    @classmethod
    def conecta(cls):
        db_host = config('DB_HOST', str)
        db_name = config('POSTGRES_DB', str)
        db_user = config('POSTGRES_USER', str)
        db_password = config('POSTGRES_PASSWORD', str)
        port = config('DB_PORT', int)

        CONN = f'postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_name}'  # noqa
        # CONN = "sqlite:///sqlite.db"
        engine = create_engine(CONN, echo=False)
        return engine

    @classmethod
    def cria_session(cls):
        engine = cls.conecta()
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        return session
