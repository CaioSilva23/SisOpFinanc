from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from conexao import Conexao


# conexao = Conexao()
engine = Conexao.conecta()

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(20), unique=True)



# class Tokens(Base):
#     __tablename__ = 'Tokens'
#     id = Column(Integer, primary_key=True)
#     id_pessoa = Column(Integer, ForeignKey('Pessoa.id'))
#     token = Column(String(200))
#     data = Column(DateTime, default=datetime.utcnow())



Base.metadata.create_all(engine)