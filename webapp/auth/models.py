import datetime
import config
import logging
import string
import random
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
    """    Classe do perfil de acesso    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(50))
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))

    user = db.relationship("User", back_populates="role")
    company = db.relationship("Company", back_populates="role")
    viewrole = db.relationship("ViewRole", back_populates="role")

    def __repr__(self) -> str:
        return f'<Role: {self.id}-{self.name}>'

    # def __init__(self, name: str, description: str, company_id: int) -> None:
    #     self.name = name
    #     self.description = description
    #     self.company_id = company_id

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


class Password(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    temporary = db.Column(db.Boolean, nullable=False, default=True)
    cont_access_temporary = db.Column(db.Integer(), nullable=True, default=0)
    expiration_date = db.Column(db.DateTime(), nullable=True)
    expirate = db.Column(db.Boolean, nullable=False, default=True)
    user = db.relationship("User", back_populates="password")

    def __repr__(self):
        return f'<Password: {self.id}-{self.password}>'

    def check_password(self, password):
        # return bcrypt.check_password_hash(self.password, password)
        return self.password == password

    def set_temporary(self, temporary) -> None:
        self.temporary = temporary

    def set_password(self, password) -> None:
        # self.password = bcrypt.generate_password_hash(password)
        self.password = password

    def set_expirate(self, expirate: bool) -> None:
        self.expirate = expirate

    def set_expiration_date(self):
        self.expiration_date = datetime.datetime.now() + datetime.timedelta(90)

    def set_cont_access_temporary(self):
        self.cont_access_temporary += 1

    def change_attributes(self, form):
        # self.password = bcrypt.generate_password_hash(password)
        self.set_password(form.password.data)
        self.set_temporary(False)
        self.cont_access_temporary = 0
        self.set_expiration_date()

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

    def verify_expiration_date(self) -> bool:
        limite = datetime.timedelta(30)
        valor =  self.expiration_date -datetime.datetime.now()

        if valor.days < 1:
            flash("A senha está expirada!", category="danger")
            return False
        elif valor < limite:
            flash("A senha está próxima de expirar, solicitamos que troque a senha", category="danger")

        return True

    @staticmethod
    def password_random(size=8, chars=string.ascii_uppercase + string.digits) -> str:
        """    Função que gera uma senha aleatório para acesso temporário    """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def password_adminluz() -> str:
        return 'Aaa-11111'


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    member_since = db.Column(db.DateTime(), nullable=True)
    last_seen = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"), nullable=False)
    role = db.relationship("Role", back_populates="user")
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"), nullable=False)
    company = db.relationship("Company", back_populates="user")

    password_id = db.Column(db.Integer(), db.ForeignKey("password.id"), nullable=False)
    password = db.relationship("Password", back_populates="user")

    def __repr__(self):
        return f'<User: {self.id}-{self.username}>'

    def user_admin(self, name: str, email: str, company_id: int, role_id: int, password_: int) -> None:
        """    Função para cadastrar as informações de administrador     """
        self.username = name
        self.email = email
        self.password_id = password_
        self.company_id = company_id
        self.role_id = role_id
        self.confirmed = True
        self.active = True
        self.member_since = datetime.datetime.now()

    def save(self):
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.autoflush = True
            db.session.add(self)
            db.session.flush()
            # db.session.commit()
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()

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

    # def set_confirmed(self, confirmed):
    #     self.confirmed = confirmed
    #     self.member_since = datetime.datetime.now()

    def set_active(self, active):
        self.active = active

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

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    @staticmethod
    def get_name_view(id_):
        view = View.query.filter_by(id=id_).first()
        return view.get_name()

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
