import functools
from flask import flash, redirect, url_for, session, abort
from flask_login import current_user
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin
from flask_jwt_extended import JWTManager
import bcrypt



class BlogAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


bcrypt = Bcrypt()
jwt = JWTManager()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Para acessar está página deve iniciar a sessão."
login_manager.login_message_category = "info"
login_manager.anonymous_user = BlogAnonymous


def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)


# def authenticate(username, password):
#     from .models import User
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         print("usuário não cadastrado!")
#         return None
#     # Do the passwords match
#     if not user.check_password(password):
#         print("senha errada!")
#         return None
#     return user
#
#
# # def identity(payload):
# #     return load_user(payload['identity'])
#
#
def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)

        return functools.update_wrapper(wraps, f)

    return real_decorator


@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)
