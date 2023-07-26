from collections import defaultdict
from handlers.auth import generate_jwt_token, get_user, auth, save_token_redis
from .base import Base


class RegisterHandler(Base):
    def post(self):
        _my_errors = defaultdict(list)

        name = self.data().get('name')
        email = self.data().get('email')
        password = self.data().get('password')
        password2 = self.data().get('password2')

        if not (name and email and password and password2):
            return self.write_error_(msg='fill in all fields')
        else:
            # valida se o email é valido
            _my_errors['email'].append('email invalid') if not self.email_valid(email=email) else None  # noqa

            # valida se já existe usuário com este email
            email_exitst = self.email_exists(email=email)
            _my_errors['email'].append('user with this email already exists') if email_exitst else None # noqa

            # valida se as senhas são iguais
            _my_errors['password'].append('passwords do not match') if password != password2 else None  # noqa

            # valida se a senha é forte
            if not self.strong_password(password):
                _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

            # valida se possui erros
            if _my_errors:
                self.set_status(404)
                return self.write(_my_errors)

            # salvo o novo usuário
            self.save_user(name=name, email=email, password=password)
            return self.write({"message": "User created successfully"})


class LoginHandler(Base):
    def post(self):
        email = self.data().get('email')
        password = self.data().get('password')
        if (email and password):
            user = self.authenticated(email=email, password=password)  # noqa
            if user:
                token = generate_jwt_token(user)
                save_token_redis(user_id=user.id, token=token)
                return self.write({'token': token})
        return self.write_error_(msg='invalid credentials')


@auth
class ChangePasswordHandler(Base):
    def patch(self):
        _my_errors = defaultdict(list)

        old_password = self.data().get('old_password')
        new_password = self.data().get('new_password')
        new_password2 = self.data().get('new_password2')

        if not (old_password and new_password and new_password2):
            return self.write_error_(msg='fill in all fields')
        else:
            # valida se as senhas são iguais
            _my_errors['password'].append('passwords do not match') if new_password != new_password2 else None  # noqa

            # valida se a senha é forte
            if not self.strong_password(new_password):
                _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

            # buscar o id do usuario a partir do token
            user_id = get_user(token=self.get_token())

            # verificar se a senha antiga desse usuário está correta
            if not self.chack_old_password(user_id=user_id, old_password=old_password):  # noqa
                _my_errors['old_password'].append("Old password invalid")

            # valida se possui erros
            if _my_errors:
                self.set_status(400)
                return self.write(_my_errors)

            # alterar a senha do usuário
            self.change_password(user_id=user_id, old_password=old_password, new_password=new_password)  # noqa
            return self.write({"message": "User change password successfully"})


@auth
class UserDetailHandler(Base):
    def get(self):
        user = self.get_detail_user()
        if user:
            return self.write({"user": {
                            "name": user.name,
                            "email": user.email,
                            "money": user.money}
                            })
        return self.write_error_(msg='user not exists')
