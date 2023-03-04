import jwt
import datetime
import config
import string
import random

def create_token(id, email, expiration=60):
    token = jwt.encode(
        {"id": id,
         "email": email,
         "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)},
        config.Config.SECRET_KEY,
        algorithm="HS256"
    )
    return token


def verify_token(tipo, token):
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
    return ''.join(random.choice(chars) for _ in range(size))




