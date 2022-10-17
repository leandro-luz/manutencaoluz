
import jwt
import datetime



def generate_token(self, expiration=600):
    reset_token = jwt.encode(
        {
            "confirm": self,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                   + datetime.timedelta(seconds=expiration)
        },
        'secret-key',
        algorithm="HS256"
    )
    return reset_token



def confirm(token):
    try:
        data = jwt.decode(
            token,
            'secret-key',
            leeway=datetime.timedelta(seconds=10),
            algorithms=["HS256"]
        )
    except:
        print('erro')
        return False
    print(data.get('confirm'))
    # if data.get('confirm') != self.id:
    #     return False
    # self.confirmed = True
    # db.session.add(self)
    return True


token = generate_confirmation_token(10)
token2 = generate_confirmation_token(100)
print(token)
confirm(token)
confirm(token2)


