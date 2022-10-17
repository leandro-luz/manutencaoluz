import logging
import click
from faker import Faker
from .auth import bcrypt
from .auth.models import User, Role, db

log = logging.getLogger(__name__)
faker = Faker()

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
        users.append(user)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            log.error("Eror inserting user: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


def register(app):
    @app.cli.command('test-data')
    def text_data():
        generate_roles()

    @app.cli.command('create-user')
    @click.argument('username')
    @click.argument('password')
    def create_user(username, password):
        user = User()
        user.username = username
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo('User {0} Added.'.format(username))
        except Exception as e:
            log.error("Fail to add new user: %s Error: %s" % (username, e))
            db.session.rollback()

    @app.cli.command('create-admin')
    @click.argument('username')
    @click.argument('password')
    def create_user(username, password):
        admin_role = Role.query.filter_by(name='admin').scalar()
        user = User()
        user.username = username
        user.set_password(password)
        user.roles.append(admin_role)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo('User {0} Added.'.format(username))
        except Exception as e:
            log.error("Fail to add new user: %s Error: %s" % (username, e))
            db.session.rollback()

    @app.cli.command('list-users')
    def list_users():
        try:
            users = User.query.all()
            for user in users:
                click.echo('{0}'.format(user.username))
        except Exception as e:
            log.error("Fail to list users Error: %s" % e)
            db.session.rollback()

    @app.cli.command('list-routes')
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo("%s %s %s" % (url.rule, url.methods, url.endpoint))
