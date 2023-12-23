import base64
import datetime
import random
import string
from urllib.parse import quote, unquote
import base64
import jwt
import pytz
from cryptography.fernet import Fernet

import config


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


def data_atual_utc():
    """Função que retorna a data atual corrigindo para o UTC"""
    local_timezone = 'America/Sao_Paulo'
    data_atual = datetime.datetime.now()
    try:
        tz = pytz.timezone(local_timezone)
        utc_offset = tz.utcoffset(data_atual).total_seconds() / 3600

        # Retornar a data corrigida
        return data_atual + datetime.timedelta(hours=utc_offset)
    except pytz.UnknownTimeZoneError:
        return data_atual


def criptografar(valor):
    # Codifica o texto para base64
    return base64.b64encode(valor.encode('utf-8')).decode('utf-8')


def descriptografar(valor):
    # Decodifica o texto base64
    if valor == '0':
        return 0
    else:
        return int(base64.b64decode(valor.encode('utf-8')).decode('utf-8'))

# def criar_objeto_fernet():
#     """Cria um objeto Fernet usando a chave específica."""
#     chave_especifica = b'4GkmZOz7sIJssA6W9ZDeKs8FjNsQViRSZqy2U0ZyC44='
#     return Fernet(chave_especifica)
#
#
# def criptografar(dados):
#     """Criptografa os dados usando o objeto Fernet."""
#     fernet = criar_objeto_fernet()
#     return quote(fernet.encrypt(dados.encode('utf-8')))
#
#
# def descriptografar(dados):
#     if dados == '0':
#         return 0
#     else:
#         fernet = criar_objeto_fernet()
#         """Descriptografa os dados criptografados usando o objeto Fernet."""
#         return int(fernet.decrypt(unquote(dados)).decode('utf-8'))
