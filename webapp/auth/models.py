from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt
import datetime
import config

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    password = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    last_seen = db.Column(db.DateTime(), nullable=True)

    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username=""):
        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # @cache.memoize(60)
    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def get_id(self):
        return str(self.id)

    def set_email(self, email):
        self.email = email

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed
        print("confirmou o email")
        self.member_since = datetime.datetime.now()

    def set_password(self, password):
        # self.password = bcrypt.generate_password_hash(password)
        self.password = password

    def check_password(self, password):
        # return bcrypt.check_password_hash(self.password, password)
        return self.password == password

    def ping(self):
        self.last_seen = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def create_token(self, expiration=600):
        token = jwt.encode(
            {"id": self.id,
             "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                    + datetime.timedelta(seconds=expiration)},
            config.Config.SECRET_KEY,
            algorithm="HS256"
        )
        return token

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(
                token,
                config.Config.SECRET_KEY,
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False
        # if data.get('id') != self.id:
        #     return False
        # self.confirmed = True
        # db.session.add(self)
        return data.get('id')


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)
