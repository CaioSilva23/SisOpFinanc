from database.models import User
from database.conexao import Conexao
from utils.valid import hash_password


session = Conexao.cria_session()


class UserQuery:

    @classmethod
    def authenticated(cls, email, password):
        user = session.query(User).filter_by(email=email, password=hash_password(password)).first()  # noqa
        return False if not user else user

    @classmethod
    def user_email_exists(cls, email):
        user = session.query(User).filter_by(email=email).first()
        return False if not user else user

    @classmethod
    def save_user(cls, name, email, password):
        user = User(name=name, email=email, password=hash_password(password))
        session.add(user)
        session.commit()
        return user

    @classmethod
    def chack_password(cls, user_id, old_password):
        user = session.query(User).filter_by(id=user_id, password=hash_password(old_password)).first()  # noqa
        return False if not user else user

    @classmethod
    def change_password(cls, user_id, old_password, new_password):
        user = cls.chack_password(user_id, old_password)
        if user:
            user.password = hash_password(new_password)
            session.commit()
            return user
