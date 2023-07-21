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


def chack_password(user_id, old_password):
    user = session.query(User).filter_by(id=user_id, password=hash_password(old_password)).first()  # noqa
    return False if not user else user


def change_password(user_id, old_password, new_password):
    user = chack_password(user_id, old_password)
    if user:
        user.password = hash_password(new_password)
        session.commit()
        return user
