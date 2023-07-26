from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Conexao():
    @classmethod
    def conecta(cls):
        db_host = 'db'
        db_name = 'postgres'
        db_user = 'postgres'
        db_password = 'postgres'
        port = 5432
    
        CONN = f'postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_name}'  # noqa
        # CONN = f'sqlite:///:dbsqliteteste'
        engine = create_engine(CONN)
        return engine

    @classmethod
    def cria_session(cls):
        engine = cls.conecta()
        
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        return session
