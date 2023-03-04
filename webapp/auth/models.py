import datetime
import config
import logging
from flask import flash
from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from webapp.plan.models import View
from flask_jwt_extended import create_access_token, get_jwt_identity
from webapp.utils.tools import password_random

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(50))
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))

    user = db.relationship("User", back_populates="role")
    company = db.relationship("Company", back_populates="role")
    viewrole = db.relationship("ViewRole", back_populates="role")

    def __repr__(self) -> str:
        return f'<Role: {self.id}-{self.name}>'

    def __init__(self, name: str, description: str, company_id: int) -> None:
        self.name = name
        self.description = description
        self.company_id = company_id

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def change_attributes(self, form):
        self.name = form.name.data
        self.description = form.description.data
        self.company_id = form.company.data

    @staticmethod
    def list_roles_by_companies(value):
        return Role.query.filter_by(company_id=value).all()


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    last_seen = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))

    role = db.relationship("Role", back_populates="user")
    company = db.relationship("Company", back_populates="user")

    def __repr__(self):
        return f'<User: {self.id}-{self.username}>'

    def user_admin(self, name: str,email: str, company_id: int, role_id: int) -> None:
        """    Função para cadastrar as informações de administrador     """
        self.username = name
        self.email = email
        self.password = password_random()
        self.company_id = company_id
        self.role_id = role_id
        self.confirmed = True
        self.active = True
        self.member_since = datetime.datetime.now()

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    # # @cache.memoize(60)
    def has_view(self, name: str) -> bool:
        """
        Verifica se a tela está cadastrada para o perfil e se está ativo
        """
        for viewrole in ViewRole.query.filter_by(role_id=self.role_id, active=True).all():
            view = View.query.filter_by(id=viewrole.view_id).one_or_none()
            if view.name == name:
                return True
        return False

    def get_id(self):
        return self.id

    def set_email(self, email):
        self.email = email

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed
        self.member_since = datetime.datetime.now()

    def set_password(self, password):
        # self.password = bcrypt.generate_password_hash(password)
        self.password = password

    def set_active(self, active):
        self.active = active

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
        return self.active

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def create_token(self, expiration=60):
        token = jwt.encode(
            {"id": self.id,
             "email": self.email,
             "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)},
            config.Config.SECRET_KEY,
            algorithm="HS256"
        )
        return token
    #
    # @staticmethod
    # def verify_token(tipo, token):
    #     try:
    #         data = jwt.decode(
    #             token,
    #             config.Config.SECRET_KEY,
    #             leeway=datetime.timedelta(seconds=10),
    #             algorithms=["HS256"]
    #         )
    #     except:
    #         return False, 0
    #     return True, data.get(tipo)

    def change_attributes(self, form, new=False):
        self.username = form.username.data
        self.email = form.email.data
        self.company_id = form.company.data
        self.role_id = form.role.data
        self.active = form.active.data
        self.password = password_random()
        self.confirmed = True
        if new:
            self.member_since = datetime.datetime.now()

    def change_active(self):
        if self.active:
            self.active = False
            flash("Usuário desativado com sucesso", category="success")
        else:
            self.active = True
            flash("Usuário ativado com sucesso", category="success")

    def get_views_role(self):
        views = []
        for viewrole in ViewRole.query.filter_by(role_id=self.role_id, active=True).all():
            view = View.query.filter_by(id=viewrole.view_id).one()
            views.append(dict(name=view.name, url=view.url, icon=view.icon))
        return views


class ViewRole(db.Model):
    """    Classe relacionamento entre Tela e Perfil    """
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))
    role = db.relationship("Role", back_populates="viewrole")
    view_id = db.Column(db.Integer(), db.ForeignKey("view.id"))
    view = db.relationship("View", back_populates="viewrole")

    def __repr__(self) -> str:
        return f'<ViewRole: {self.id}-{self.id}>'

    def __init__(self, role_id: int, view_id: int, active: bool) -> None:
        self.role_id = role_id
        self.view_id = view_id
        self.active = active

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def change_attributes(self, form):
        self.role_id = form.user.data
        self.view_id = form.view.data

    def get_name_view(self, id):
        view = View.query.filter_by(id=id).first()
        return view.get_name()

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    @staticmethod
    def change_roles(active: bool, *args):
        [[[ViewRole.save_change(active, item) for item in posicao] for posicao in id_] for id_ in args]

    @staticmethod
    def save_change(active: bool, kwargs) -> None:
        viewrole = ViewRole.query.filter_by(role_id=kwargs['role_id'], view_id=kwargs['view_id']).one_or_none()

        if viewrole:  # se exister a tela para o perfil
            if active:  # é para ativar
                if kwargs['role_name'] == 'admin':  # o perfil é administrador
                    viewrole.active = True
            else:  # o perfil não é administrador
                viewrole.active = False  # desativa para qualquer perfil
        else:
            viewrole = ViewRole()
            viewrole.role_id = kwargs['role_id']
            viewrole.view_id = kwargs['view_id']
            if kwargs['role_name'] == 'admin':  # o perfil é administrador
                viewrole.active = True  # deixa ativa a tela
            else:  # o perfil não é administrador
                viewrole.active = False  # deixa desativada a tela

        db.session.add(viewrole)
        db.session.commit()
