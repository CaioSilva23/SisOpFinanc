from database.models import User
from database.conexao import Conexao
from utils.valid import hash_password


session = Conexao.cria_session()


def authenticated(email, password):
    user = session.query(User).filter_by(email=email, password=hash_password(password)).first()  # noqa
    return False if not user else user


def user_email_exists(email):
    user = session.query(User).filter_by(email=email).first()
    return False if not user else user


def save_user(email, password):
    user = User(email=email, password=hash_password(password))
    session.add(user)
    session.commit()
