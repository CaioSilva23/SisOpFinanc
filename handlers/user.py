import tornado.ioloop
import tornado.web
from collections import defaultdict
from database.query_user import authenticated, user_email_exists, save_user, chack_password, change_password
from handlers.auth import generate_jwt_token, get_user
import json
from utils.valid import strong_password, email_valid
from utils.send_mail import send_mail
from utils.gererate_password import generate_temp_password


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            json_data = json.loads(self.request.body)
            email = json_data.get('email')
            password = json_data.get('password')
            if email and password:
                user = authenticated(email=email, password=password)
                if user:
                    token = generate_jwt_token(user)
                    return self.write({'token': token})
        except Exception:
            pass
        self.set_status(400)
        return self.write({"error": "invalid credentials"})


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        _my_errors = defaultdict(list)
        try:
            json_data = json.loads(self.request.body)
            email = json_data.get('email')
            password = json_data.get('password')
            password2 = json_data.get('password2')

            if email and password and password2:
                # valida se o email é valido
                _my_errors['email'].append('email invalid') if not email_valid(email=email) else None  # noqa

                # valida se já existe usuário com este email
                user = user_email_exists(email=email)
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
        except Exception:
            pass
        self.set_status(400)
        return self.write({"error": "fill in all fields"})


class ChangePasswordHandler(tornado.web.RequestHandler):
    def get_token(self):
        token = self.request.headers.get('Authorization').split()[1]
        return token

    def post(self):
        _my_errors = defaultdict(list)
        try:
            json_data = json.loads(self.request.body)
            old_password = json_data.get('old_password')
            new_password = json_data.get('new_password')
            new_password2 = json_data.get('new_password2')

            if old_password and new_password and new_password2:
                # valida se as senhas são iguais
                _my_errors['password'].append('passwords do not match') if new_password != new_password2 else None  # noqa

                # valida se a senha é forte
                if not strong_password(new_password):
                    _my_errors['password'].append('No mínimo 8 caracteres, possuir pelo menos uma letra minuscula, uma letra maiúscula e um número')  # noqa

                # buscar o id do usuario a partir do token
                user_id = get_user(token=self.get_token())

                # verificar se a senha antiga desse usuário está correta
                user = chack_password(user_id=user_id, old_password=old_password)  # noqa

                # alterar a senha do usuário
                if user:
                    change_password(user_id=user_id, old_password=old_password, new_password=new_password)  # noqa
                else:
                    _my_errors['old_password'].append("Old password invalid")

                # valida se possui erros
                if _my_errors:
                    self.set_status(400)
                    return self.write(_my_errors)

                # altera senha de usuário
                return self.write({"message": "User change password successfully"})
            
        except Exception:
            pass
        self.set_status(400)
        return self.write({"error": "fill in all fields"})

    

# temp_password = None
# class ResetPassword(tornado.web.RequestHandler):
#     def post(self):
#         _my_errors = defaultdict(list)

#         global temp_password

#         try:
#             data = self.request.body
#             json_data = json.loads(data)
#             email = json_data.get('email')

#             # valida se o email é valido
#             _my_errors['email'].append('email invalid') if not email_valid(email=email) else None  # noqa

#             # valida se possui erros
#             if _my_errors:
#                 self.set_status(400)
#                 return self.write(_my_errors)

#             # send email
#             # retorna true se foi enviado com sucesso
#             token = generate_temp_password()
#             url = f'http://127.0.0.1:8888/reset-password-token/{token}'

#             mail = send_mail(
#                 to_email=email,
#                 subject='Reset Password',
#                 body=f'Clique no link para resetar sua senha, {url}')

#             if mail:
#                 return self.write({"message": "reset password send for email"})
#         except Exception:
#             return self.write({"error": "error for send for email"})
