import tornado.ioloop
import tornado.web
from collections import defaultdict
from database.query_user import authenticated, user_email_exists, save_user
from apps.auth import generate_jwt_token
import json
from utils.valid import strong_password, email_valid


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body
        json_data = json.loads(data)
        email = json_data.get('email')
        password = json_data.get('password')

        if email and password:
            user = authenticated(email=email, password=password)
            if user:
                token = generate_jwt_token(user)
                return self.write({'token': token})
            # else:
            #     self.set_status(400)
        #         self.write({'error': 'invalid credentials'})
        # else:
        self.set_status(400)
        return self.write({"error": "invalid credentials"})


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        _my_errors = defaultdict(list)
        data = self.request.body
        json_data = json.loads(data)
        email = json_data.get('email')
        password = json_data.get('password')
        password2 = json_data.get('password2')

        user = user_email_exists(email=email)

        # valida se o email é valido
        _my_errors['email'].append('email invalid') if not email_valid(email=email) else None  # noqa

        # valida se já existe usuário com este email
        _my_errors['email'].append('user with this email already exists') if user else None # noqa

        # valida se as senhas são iguais
        _my_errors['password'].append('passwords do not match') if password != password2 else None  # noqa

        # valida se a senha é forte
        if not strong_password(password):
            _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

        # valida se possui erros
        if _my_errors:
            self.set_status(400)
            return self.write(_my_errors)

        # salvo o novo usuário
        save_user(email=email, password=password)

        return self.write({"message": "User created successfully"})
