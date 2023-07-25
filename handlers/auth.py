import jwt
import datetime
import redis

# Configurar a conexão com o Redis (conforme mencionado anteriormente)
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


def save_token_redis(user_id, token):
    #  3600 segundos = 1 hora
    tempo_expiracao = 3600

    # Armazenar o token no Redis com o ID do usuário como chave
    redis_key = f"user_token:{user_id}"
    redis_client.setex(name=redis_key, time=tempo_expiracao, value=token)


# Chave secreta para assinar o token (mantenha-a segura e não compartilhe publicamente)
AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_METHOD = 'bearer'
SECRET_KEY = "my_secret_key"
INVALID_HEADER_MESSAGE = "invalid header authorization"
MISSING_AUTHORIZATION_KEY = "Missing authorization"
AUTHORIZTION_ERROR_CODE = 401


jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


def is_valid_header(parts):
    """
        Validate the header
    """
    if parts[0].lower() != AUTHORIZATION_METHOD:
        return False
    elif len(parts) == 1:
        return False
    elif len(parts) > 2:
        return False

    return True


def return_auth_error(handler, message):
    """
        Return authorization error
    """
    handler._transforms = []
    handler.set_status(AUTHORIZTION_ERROR_CODE)
    handler.write(message)
    handler.finish()


def return_header_error(handler):
    """
        Returh authorization header error
    """
    return_auth_error(handler, INVALID_HEADER_MESSAGE)


def auth(handler_class):
    """
        Tornado JWT Auth Decorator
    """
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):

            auth = handler.request.headers.get(AUTHORIZATION_HEADER)
            if auth:
                parts = auth.split()

                if not is_valid_header(parts):
                    return_header_error(handler)
                token = parts[1]
                try:
                    # Decodificar o token usando a chave secreta
                    payload = jwt.decode(
                                    token,
                                    SECRET_KEY,
                                    options=jwt_options,
                                    algorithms='HS256'
                                )

                    user_id = payload['user_id']

                    # Verificar se o token está no Redis
                    token_salvo = redis_client.get(str(user_id))

                    if token_salvo and token_salvo.decode('utf-8') == token:
                        pass
                    else:
                        return 'token invalido'
                except Exception as err:
                    return_auth_error(handler, str(err))
            else:
                handler._transforms = []
                handler.write(MISSING_AUTHORIZATION_KEY)
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class


def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # noqa Token expira 1h
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def get_user(token):
    try:
        user = jwt.decode(
                    token,
                    SECRET_KEY,
                    options=jwt_options,
                    algorithms='HS256'
                )
        return user.get('user_id')
    except Exception:
        pass
