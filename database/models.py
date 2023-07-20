from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from database.conexao import Conexao

engine = Conexao.conecta()
Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String(20), unique=True)
    password = Column(String(20))


class Acao(Base):
    __tablename__ = 'Acao'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    value = Column(Float)
    user_id = Column(Integer, ForeignKey('User.id'))


Base.metadata.create_all(engine)
