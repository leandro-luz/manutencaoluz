import logging
import click
from faker import Faker
from .usuario import bcrypt
from .usuario.models import Usuario, Perfil, db

log = logging.getLogger(__name__)
# faker = Faker()

# fake_users = [
#     {'razao_social': 'user_default', 'role': 'default'},
#     {'razao_social': 'user_poster', 'role': 'poster'},
#     {'razao_social': 'admin', 'role': 'admin'}
# ]
# fake_roles = ['default', 'poster', 'admin']


# def generate_roles():
#     roles = list()
#     for rolename in fake_roles:
#         role = Perfil.query.filter_by(razao_social=rolename).first()
#         if role:
#             roles.append(role)
#             continue
#         role = Perfil(rolename)
#         roles.append(role)
#         db.session.add(role)
#         try:
#             db.session.commit()
#         except Exception as e:
#             log.error("Erro inserting role: %s, %s" % (str(role), e))
#             db.session.rollback()
#     return roles
#
#
# def generate_users():
#     users = list()
#     for item in fake_users:
#         user = Usuario.query.filter_by(razao_social=item['razao_social']).first()
#         if user:
#             users.append(user)
#             continue
#         user = Usuario()
#         poster = Perfil.query.filter_by(razao_social=item['role']).one()
#         user.roles.append(poster)
#         user.razao_social = item['razao_social']
#         user.senha = bcrypt.generate_password_hash("senha")
#         users.append(user)
#         try:
#             db.session.add(user)
#             db.session.commit()
#         except Exception as e:
#             log.error("Eror inserting user: %s, %s" % (str(user), e))
#             db.session.rollback()
#     return users


def register(app):
    # @app.cli.command('test-data')
    # def text_data():
    #     generate_roles()

    # @app.cli.command('create-user')
    # @click.argument('razao_social')
    # @click.argument('senha')
    # def create_user(razao_social, senha):
    #     user = Usuario()
    #     user.razao_social = razao_social
    #     user.set_password(senha)
    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #         click.echo('Usuario {0} Added.'.format(razao_social))
    #     except Exception as e:
    #         log.error("Fail to add new user: %s Error: %s" % (razao_social, e))
    #         db.session.rollback()
    #
    # @app.cli.command('create-admin')
    # @click.argument('razao_social')
    # @click.argument('senha')
    # def create_user(razao_social, senha):
    #     admin_role = Perfil.query.filter_by(razao_social='admin').scalar()
    #     user = Usuario()
    #     user.razao_social = razao_social
    #     user.set_password(senha)
    #     user.roles.append(admin_role)
    #     try:
    #         db.session.add(user)
    #         db.session.commit()
    #         click.echo('Usuario {0} Added.'.format(razao_social))
    #     except Exception as e:
    #         log.error("Fail to add new user: %s Error: %s" % (razao_social, e))
    #         db.session.rollback()

    # @app.cli.command('list-users')
    # def list_users():
    #     try:
    #         users = Usuario.query.all()
    #         for user in users:
    #             click.echo('{0}'.format(user.razao_social))
    #     except Exception as e:
    #         log.error("Fail to list users Error: %s" % e)
    #         db.session.rollback()

    @app.cli.command('list-routes')
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo("%s %s %s" % (url.rule, url.methods, url.endpoint))
