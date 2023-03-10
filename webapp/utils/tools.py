import jwt
import datetime
import config
import string
import random


def create_token(id_, email, expiration=60):
    """    Função que gera um token para acesso externo    """
    token = jwt.encode(
        {"id": id_,
         "email": email,
         "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)},
        config.Config.SECRET_KEY,
        algorithm="HS256"
    )
    return token


def verify_token(tipo, token):
    """    Função que válida o token recebido de um acesso externo    """
    try:
        data = jwt.decode(
            token,
            config.Config.SECRET_KEY,
            leeway=datetime.timedelta(seconds=10),
            algorithms=["HS256"]
        )
    except:
        return False, 0
    return True, data.get(tipo)


def password_random(size=8, chars=string.ascii_uppercase + string.digits) -> str:
    """    Função que gera uma senha aleatório para acesso temporário    """
    return ''.join(random.choice(chars) for _ in range(size))
