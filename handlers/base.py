import tornado.ioloop
import tornado.web
import json
from json import JSONDecodeError
from handlers.auth import get_user
import re
from hashlib import sha256
from database.conexao import Conexao
from database.models import User, Acao, Operacao
from sqlalchemy import func

session = Conexao.cria_session()


class Base(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')  # noqa
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")  # noqa

    def prepare(self):
        pass

    def data(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError:
            return {}

    """tools to user"""
    def get_user(self):
        return get_user(token=self.get_token())

    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    def strong_password(self, password):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
        if not regex.match(password):
            return False
        return True

    def email_valid(self, email):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  # noqa
        if not re.fullmatch(regex, email):
            return False
        return True

    def email_exists(self, email):
        email = session.query(User).filter_by(email=email).first()
        return False if not email else True

    def save_user(self, name, email, password):
        user = User(name=name, email=email, password=self.hash_password(password))  # noqa
        session.add(user)
        session.commit()
        session.close()
        return user

    def authenticated(self, email, password):
        user = session.query(User).filter_by(email=email, password=self.hash_password(password)).first()  # noqa
        return False if not user else user

    def chack_old_password(self, user_id, old_password):
        user = session.query(User).filter_by(id=user_id, password=self.hash_password(old_password)).first()  # noqa
        return False if not user else user

    def change_password(self, user_id, old_password, new_password):
        user = self.chack_old_password(user_id, old_password)
        if user:
            user.password = self.hash_password(new_password)
            session.commit()
            session.close
            return user

    def hash_password(self, password):
        return sha256(password.encode('utf-8')).hexdigest()
    """end tools to user"""

    """tools to actions"""
    def acoes_list(self):
        return session.query(Acao).filter(Acao.stock > 0).all()

    def save_acao(self, name, description, price_unit, stock):
        acao = Acao(
            name=name,
            description=description,
            price_unit=price_unit,
            stock=stock,
        )
        acao = session.add(acao)
        session.commit()
        session.close
        return acao

    def acao_get_id(self, id):
        return session.query(Acao).filter_by(id=id).first()

    def acao_update_quantity(self, id, new_quantity):
        acao = self.acao_get_id(id=id)
        acao.stock -= new_quantity
        session.commit()
        session.close()
        return acao

    def list_acoes_for_user(self):
        acoes_compradas = (
            session.query(
                Acao,
                func.sum(Operacao.quantity).label('quantity'),
            )
            .join(Operacao)
            .filter(Operacao.user_id == self.get_user(),
                    Operacao.type_operation == 'Compra')
            .group_by(Acao)
            .all()
        )
        return acoes_compradas
    """end tools to actions"""

    """tools to operations"""
    def list_operations(self):
        return session.query(Operacao).filter_by(user_id=self.get_user())

    def save_operation(self, acao_id, type_operation, quantity):
        try:
            print("11")
            self.acao_update_quantity(id=acao_id, new_quantity=quantity)

            acao = self.acao_get_id(id=acao_id)
            operacao = Operacao(
                user_id=self.get_user(),
                acao_id=acao_id,
                type_operation=type_operation,
                quantity=quantity,
                price_total=acao.price_unit * quantity,
                date=func.now()
            )
            session.add(operacao)
            session.commit()
        except Exception as e:
            print(f"{e}")
            session.rollback()
        finally:
            print("233")
            session.close()

    def operation_get_id(self, id):
        return session.query(Operacao).filter_by(id=id, user_id=self.get_user()).first()  # noqa
