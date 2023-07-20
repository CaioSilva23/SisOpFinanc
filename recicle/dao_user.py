# import tornado.ioloop
# import tornado.web
# from models import User
# from conexao import Conexao
# import json
# from auth import generate_jwt_token

# #  Configuração do SQLAlchemy
# session = Conexao.cria_session()


# class LoginHandler(tornado.web.RequestHandler):
#     def post(self):
#         # Aqui, você autentica o usuário e obtém o objeto `user`
#         user = session.query(User).filter_by(name='Cesar', email='caio@mail.com').first()
        
#         if user:
#             token = generate_jwt_token(user)
#             self.write({'token': token})
#         else:
#             self.set_status(401)
#             self.write({'error': 'Usuário ou senha inválidos'})



# #SECRET = 'my_secret_key'
# # class AuthHandler(tornado.web.RequestHandler):
# #     """
# #         Handle to auth method.
# #         This method aim to provide a new authorization token
# #         There is a fake payload (for tutorial purpose)
# #     """
# #     def prepare(self):
# #         """
# #             Encode a new token with JSON Web Token (PyJWT)
# #         """
# #         self.encoded = jwt.encode({
# #             'some': 'payload',
# #             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=600)},
# #             SECRET,
# #             algorithm='HS256'
# #         )

# #     def get(self, *args, **kwargs):
# #         """
# #             return the generated token
# #         """
# #         response = {'token': self.encoded}
# #         print(response)
# #         print(self.encoded.encode().decode())
# #         self.write(response)






# class UsersHandler(tornado.web.RequestHandler):
#     async def get(self):
#         users = session.query(User).all()
#         self.write({"users": [{"id": user.id, "name": user.name, "email": user.email} for user in users]})  # noqa

#     async def post(self):
#         data = self.request.body
#         json_data = json.loads(data)
#         name = json_data.get('name')
#         email = json_data.get('email')
#         user = User(name=name, email=email)
#         session.add(user)
#         session.commit()
#         self.write({"message": "User created successfully"})

        
# # class UserHandler(tornado.web.RequestHandler):
# #     async def get(self, user_id):
# #         user = await db.session.execute(db.select(User).where(User.id == user_id))
# #         user = user.scalar()
# #         if user:
# #             self.write({"id": user.id, "name": user.name, "email": user.email})
# #         else:
# #             self.write({"message": "User not found"})

# #     async def put(self, user_id):
# #         name = self.get_argument("name")
# #         email = self.get_argument("email")
# #         user = await db.session.execute(db.select(User).where(User.id == user_id))
# #         user = user.scalar()
# #         if user:
# #             user.name = name
# #             user.email = email
# #             await db.session.commit()
# #             self.write({"message": "User updated successfully"})
# #         else:
# #             self.write({"message": "User not found"})

# #     async def delete(self, user_id):
# #         user = await db.session.execute(db.select(User).where(User.id == user_id))
# #         user = user.scalar()
# #         if user:
# #             db.session.delete(user)
# #             await db.session.commit()
# #             self.write({"message": "User deleted successfully"})
# #         else:
# #             self.write({"message": "User not found"})


