import logging
import os
from webapp import create_app
from webapp import db
from webapp.auth.models import Role, User

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

roles_lista = ['default', 'admin']
user_lista = [
    {'username': 'leandro',
     'email': 'engleoluz@hotmail.com',
     'password': 'aaa11111',
     'role': 'default'},
    {'username': 'danylo',
     'email': 'luzdanylo@gmail.com',
     'password': '12345678',
     'role': 'default'}
]


def generate_roles():
    roles = list()
    for rolename in roles_lista:
        role = Role.query.filter_by(name=rolename).first()
        if role:
            roles.append(role)
            continue
        role = Role(rolename)
        roles.append(role)
        db.session.add(role)
        try:
            db.session.commit()
            print('Regra inserida:', role.name)
        except Exception as e:
            log.error("Erro ao inserir a regra: %s, %s" % (str(role), e))
            db.session.rollback()
    return roles


def generate_users():
    users = list()
    for item in user_lista:
        user = User.query.filter_by(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        role = Role.query.filter_by(name=item['role']).one()
        user.username = item['username']
        user.email = item['email']
        user.password = item['password']
        user.confirmed = True
        user.role_id = role.id
        users.append(user)
        try:
            db.session.add(user)
            db.session.commit()
            print('Usuário inserido:', user.username)
        except Exception as e:
            log.error("Erro ao inserir usuário: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


generate_roles()
generate_users()
