from collections import defaultdict
from queries.query_user import UserQuery
from handlers.auth import generate_jwt_token, get_user, jwtauth
from utils.valid import strong_password, email_valid
from http import HTTPStatus
from .base import UserBase
import tornado.web


class RegisterHandler(UserBase):
    def post(self):
        _my_errors = defaultdict(list)

        email = self.data().get('email')
        password = self.data().get('password')
        password2 = self.data().get('password2')

        if not (email and password and password2):
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.write({"error": "fill in all fields"})
        else:
            # valida se o email é valido
            _my_errors['email'].append('email invalid') if not email_valid(email=email) else None  # noqa

            # valida se já existe usuário com este email
            user = UserQuery.user_email_exists(email=email)
            _my_errors['email'].append('user with this email already exists') if user else None # noqa

            # valida se as senhas são iguais
            _my_errors['password'].append('passwords do not match') if password != password2 else None  # noqa

            # valida se a senha é forte
            if not strong_password(password):
                _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

            # valida se possui erros
            if _my_errors:
                self.set_status(HTTPStatus.BAD_REQUEST)
                return self.write(_my_errors)

            # salvo o novo usuário
            UserQuery.save_user(email=email, password=password)
            return self.write({"message": "User created successfully"})


class LoginHandler(UserBase):
    def post(self):
        email = self.data().get('email')
        password = self.data().get('password')
        if (email and password):
            user = UserQuery.authenticated(email=email, password=password)  # noqa
            if user:
                token = generate_jwt_token(user)
                return self.write({'token': token})
        self.set_status(HTTPStatus.BAD_REQUEST)
        return self.write({"error": "invalid credentials"})


@jwtauth
class ChangePasswordHandler(UserBase):
    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    def patch(self):
        _my_errors = defaultdict(list)

        old_password = self.data().get('old_password')
        new_password = self.data().get('new_password')
        new_password2 = self.data().get('new_password2')

        if not (old_password and new_password and new_password2):
            self.set_status(HTTPStatus.BAD_REQUEST)
            return self.write({"error": "fill in all fields"})
        else:
            # valida se as senhas são iguais
            _my_errors['password'].append('passwords do not match') if new_password != new_password2 else None  # noqa

            # valida se a senha é forte
            if not strong_password(new_password):
                _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

            # buscar o id do usuario a partir do token
            user_id = get_user(token=self.get_token())

            # verificar se a senha antiga desse usuário está correta
            user = UserQuery.chack_password(user_id=user_id, old_password=old_password)  # noqa

            # alterar a senha do usuário
            if user:
                UserQuery.change_password(user_id=user_id, old_password=old_password, new_password=new_password)  # noqa
            else:
                _my_errors['old_password'].append("Old password invalid")

            # valida se possui erros
            if _my_errors:
                self.set_status(400)
                return self.write(_my_errors)

            # altera senha de usuário
            return self.write({"message": "User change password successfully"})
