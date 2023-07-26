import tornado.ioloop
import tornado.web
import json
from json import JSONDecodeError
from handlers.auth import get_user
import re
from hashlib import sha256
from database.conexao import Conexao
from database.models import User, Acao, Operacao, StokAction
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

    def write_error_(self, msg):
        self.set_status(404)
        self.write({'error': msg})

    def data(self):
        try:
            return json.loads(self.request.body)
        except JSONDecodeError:
            return {}

    """tools to user"""
    def get_user(self):
        return get_user(token=self.get_token())

    def get_detail_user(self):
        user = session.query(User).filter_by(id=self.get_user()).first()
        return user

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
        return session.query(Acao).all()

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

    def list_acoes_for_user(self):
        stock_actions = session.query(StokAction).filter(StokAction.quantity > 0, StokAction.user_id==self.get_user()).all()  # noqa
        return stock_actions
    """end tools to actions"""

    """tools to operations"""
    def list_operations(self):
        return session.query(Operacao).filter_by(user_id=self.get_user())
    
    def get_user_dono(self, id):
        """busca o dono da ação em oferta"""
        return session.query(User).filter_by(id=id).first()

    def save_operation_purchase(self, user, acao, quantity):
        try:
            if acao.oferta:
                dono = self.get_user_dono(id=int(acao.oferta))
                dono.money += acao.price_unit * quantity
            user.money -= acao.price_unit * quantity
            acao.stock -= quantity
            operacao = Operacao(
                user_id=self.get_user(),
                acao_id=acao.id,
                type_operation='Compra',
                quantity=quantity,
                price_total=acao.price_unit * quantity,
                price_unit=acao.price_unit,
                date=func.now()
            )

            stockaction = session.query(StokAction).filter_by(acao_id=acao.id, user_id=self.get_user()).first()  # noqa
            if stockaction:
                stockaction.quantity += quantity
            else:
                stockaction = StokAction(
                    user_id=self.get_user(),
                    acao_id=acao.id,
                    quantity=quantity,
                )
            session.add(stockaction)
            session.add(operacao)
            session.commit()
            return True
        except Exception:
            session.rollback()
            session.close
            return False

    def save_operation_sale(self, quantity, price_venda, stock_action):
        try:
            stock_action.quantity -= quantity
            operacao = Operacao(
                user_id=self.get_user(),
                acao_id=stock_action.acao.id,
                type_operation='Venda',
                quantity=quantity,
                price_total=price_venda * quantity,
                price_unit=price_venda,
                date=func.now()
            )
            acao = Acao(
                    oferta=self.get_user(),
                    name=stock_action.acao.name,
                    description=stock_action.acao.description,
                    price_unit=price_venda,
                    stock=quantity
                )
            session.add(operacao)
            session.add(acao)
            session.commit()
            return True
        except Exception as e:
            self.write(f'----------------{e}')
            session.rollback()
            session.close
            return False

    def stock_action_get(self, id):
        stock_action = session.query(StokAction).filter_by(id=id, user_id=self.get_user()).first()  # noqa
        return stock_action

    def operation_get_id(self, id):
        operacao = session.query(Operacao).filter_by(id=id, user_id=self.get_user()).first()  # noqa
        return operacao
