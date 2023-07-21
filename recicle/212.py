import tornado.ioloop
import tornado.web
import random
import string

# Informações do único usuário (substitua por seus dados)
user = {
    'username': 'usuario1',
    'email': 'usuario1@example.com',
    'senha': 'senha1'
}

temp_password = None


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ResetPasswordHandler(tornado.web.RequestHandler):
    def post(self):
        global temp_password
        email = self.get_argument('email')

        if email == user['email']:
            temp_password = generate_temp_password()
            # Aqui, você pode enviar o email com o link contendo o token de redefinição
            self.write(f"Um link para redefinir sua senha foi enviado para {email}.")
        else:
            self.write("Email não encontrado.")


class ResetPasswordTokenHandler(tornado.web.RequestHandler):
    def post(self, token):
        global temp_password
        if temp_password and token == temp_password:
            new_password = self.get_argument('new_password')
            user['senha'] = new_password
            temp_password = None
            self.write("Senha redefinida com sucesso!")
        else:
            self.write("Token inválido ou expirado.")


def generate_temp_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(8))


def make_app():
    return tornado.web.Application([
        (r'/', IndexHandler),
        (r'/reset_password', ResetPasswordHandler),
        (r'/reset_password/(.*)', ResetPasswordTokenHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
