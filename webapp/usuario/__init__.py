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
        self.nome = 'Guest'


bcrypt = Bcrypt()
jwt = JWTManager()

login_manager = LoginManager()
login_manager.login_view = "usuario.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Para acessar está página deve iniciar a sessão."
login_manager.login_message_category = "info"
login_manager.anonymous_user = BlogAnonymous


def criar_modulo(app, **kwargs) -> None:
    """    Cria o módulo para controlador Auth - controle de de acessos    """
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    from .controllers import usuario_blueprint
    app.register_blueprint(usuario_blueprint)


def has_view(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.ativo:
                if current_user.tela_permitida(name):
                    return f(*args, **kwargs)
                else:
                    abort(403)
            else:
                return redirect(url_for('usuario.logout'))

        return functools.update_wrapper(wraps, f)

    return real_decorator


@login_manager.user_loader
def load_user(userid: int) -> int:
    """     Retorna o id do usuário     """
    from .models import Usuario
    return Usuario.query.get(userid)
