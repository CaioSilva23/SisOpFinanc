from sqlalchemy import Column, \
                        Integer, \
                        String, \
                        Float, \
                        DateTime, \
                        ForeignKey, \
                        CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database.conexao import Conexao

engine = Conexao.conecta()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    money = Column(Float, default=100)

    operacoes = relationship('Operacao', back_populates='user')
    stockactions = relationship('StokAction', back_populates='user')


class StokAction(Base):
    __tablename__ = 'stockactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    acao_id = Column(Integer, ForeignKey('acoes.id'), nullable=False)
    price_unit = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship('User', back_populates='stockactions')
    acao = relationship('Acao', back_populates='stockactions')


class Acao(Base):
    __tablename__ = 'acoes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    stock = Column(Integer, nullable=False)
    price_unit = Column(Float, nullable=False)
    oferta = Column(Integer, nullable=True)

    operacoes = relationship('Operacao', back_populates='acao')
    stockactions = relationship('StokAction', back_populates='acao')


# classe de Operações de Compra e Venda
class Operacao(Base):
    __tablename__ = 'operacoes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    acao_id = Column(Integer, ForeignKey('acoes.id'), nullable=False)
    type_operation = Column(String, nullable=False)  # Compra ou venda
    status = Column(String, nullable=False, default="Concluído")
    quantity = Column(Integer, nullable=False)
    price_total = Column(Float, nullable=False)
    price_unit = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    __table_args__ = (
        CheckConstraint(type_operation.in_(('Compra', 'Venda'))),
    )
    __table_args__ = (
        CheckConstraint(status.in_(('Concluído', 'Pendente'))),
    )
    user = relationship('User', back_populates='operacoes')
    acao = relationship('Acao', back_populates='operacoes')


Base.metadata.create_all(engine)
