import logging
import random
from faker import Faker
from webapp import create_app
from webapp import db
from webapp.auth.models import User, Role
from webapp.auth import bcrypt
from config import DevConfig

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
app = create_app(DevConfig)
app.app_context().push()

Faker.seed(0)
faker = Faker('pt_BR')
faker.seed_locale('pt_BR', 0)

fake_users = [
    {'username': 'user_default', 'role': 'default'},
    {'username': 'user_poster', 'role': 'poster'},
    {'username': 'admin', 'role': 'admin'}
]
fake_roles = ['default', 'poster', 'admin']


def generate_roles():
    roles = list()
    for rolename in fake_roles:
        role = Role.query.filter_by(name=rolename).first()
        if role:
            roles.append(role)
            continue
        role = Role(rolename)
        roles.append(role)
        db.session.add(role)
        try:
            db.session.commit()
        except Exception as e:
            log.error("Erro inserting role: %s, %s" % (str(role), e))
            db.session.rollback()
    return roles


def generate_users():
    users = list()
    for item in fake_users:
        user = User.query.filter_by(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        poster = Role.query.filter_by(name=item['role']).one()
        user.roles.append(poster)
        user.username = item['username']
        user.password = bcrypt.generate_password_hash("password")
        # user.email = 'email@teste.com.br'
        # user.confirmed = True
        users.append(user)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            log.error("Eror inserting user: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


generate_roles()
generate_users()
