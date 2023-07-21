
# from utils.send_mail import send_mail
# from utils.gererate_password import generate_temp_password
# # temp_password = None
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
