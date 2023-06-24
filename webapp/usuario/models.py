import datetime
import config
import logging
import string
import random
from flask import flash
from webapp.usuario import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from webapp.contrato.models import Tela
from flask_jwt_extended import create_access_token, get_jwt_identity
from webapp.utils.tools import password_random


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class Perfil(db.Model):
    """    Classe do perfil de acesso    """
    __tablename__ = 'perfil'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), unique=False, index=True)
    descricao = db.Column(db.String(50))

    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="perfil")
    empresa = db.relationship("Empresa", back_populates="perfil")
    telaperfil = db.relationship("Telaperfil", back_populates="perfil")

    def __repr__(self) -> str:
        return f'<Perfil: {self.id}-{self.nome}>'

    def salvar(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def alterar_atributos(self, form, empresa_id):
        self.nome = form.nome.data
        self.descricao = form.descricao.data
        self.empresa_id = empresa_id

    @staticmethod
    def listar_regras_by_empresa(empresa_id: int):
        return Perfil.query.filter_by(empresa_id=empresa_id).all()


class Senha(db.Model):
    __tablename__ = 'senha'
    id = db.Column(db.Integer(), primary_key=True)
    senha = db.Column(db.String(50), nullable=False, index=True)
    senha_temporaria = db.Column(db.Boolean, nullable=False, default=True)
    contador_acesso_temporario = db.Column(db.Integer(), nullable=True, default=0)
    data_expiracao = db.Column(db.DateTime(), nullable=True)
    senha_expira = db.Column(db.Boolean, nullable=False, default=True)

    usuario = db.relationship("Usuario", back_populates="senha")

    def __repr__(self):
        return f'<Senha: {self.id}-{self.senha}>'

    def verificar_senha(self, senha):
        # return bcrypt.check_password_hash(self.senha, senha)
        return self.senha == senha

    def alterar_senha_temporaria(self, temporario: bool) -> None:
        self.senha_temporaria = temporario

    def alterar_senha(self, senha) -> None:
        # self.senha = bcrypt.generate_password_hash(senha)
        self.senha = senha

    def alterar_expiravel(self, senha_expira: bool) -> None:
        self.senha_expira = senha_expira

    def alterar_data_expiracao(self):
        self.data_expiracao = datetime.datetime.now() + datetime.timedelta(90)

    def alterar_contador_accesso_temporario(self):
        self.contador_acesso_temporario += 1

    def alterar_atributos(self, form):
        # self.senha = bcrypt.generate_password_hash(senha)
        self.alterar_senha(form.senha.data)
        self.alterar_senha_temporaria(False)
        self.contador_acesso_temporario = 0
        self.alterar_data_expiracao()

    def salvar(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def verificar_data_expiracao(self) -> bool:
        limite = datetime.timedelta(30)
        valor = self.data_expiracao - datetime.datetime.now()

        if valor.days < 1:
            flash("A senha está expirada!", category="danger")
            return False
        elif valor < limite:
            flash("A senha está próxima de expirar, solicitamos que troque a senha", category="danger")

        return True

    @staticmethod
    def senha_aleatoria(size=8, chars=string.ascii_uppercase + string.digits) -> str:
        """    Função que gera uma senha aleatório para acesso temporário    """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def password_adminluz() -> str:
        return 'Aaa-11111'


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=False)
    data_assinatura = db.Column(db.DateTime(), nullable=True)
    data_ultima_entrada = db.Column(db.DateTime(), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    perfil_id = db.Column(db.Integer(), db.ForeignKey("perfil.id"), nullable=False)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)
    senha_id = db.Column(db.Integer(), db.ForeignKey("senha.id"), nullable=False)

    perfil = db.relationship("Perfil", back_populates="usuario")
    empresa = db.relationship("Empresa", back_populates="usuario")
    senha = db.relationship("Senha", back_populates="usuario")
    ordemservico = db.relationship("OrdemServico", back_populates="usuario")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="usuario")

    def __repr__(self):
        return f'<Usuario: {self.id}-{self.nome}>'

    def usuario_administrador(self, nome: str, email: str, empresa_id: int, perfil_id: int, senha_id: int) -> None:
        """    Função para cadastrar as informações de administrador     """
        self.nome = nome
        self.email = email
        self.senha_id = senha_id
        self.empresa_id = empresa_id
        self.perfil_id = perfil_id
        self.ativo = True
        self.data_assinatura = datetime.datetime.now()

    def salvar(self) -> bool:
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
    def tela_permitida(self, nome: str) -> bool:
        """
        Verifica se a tela está cadastrada para o perfil e se está ativo
        """
        for telacontrato in Telaperfil.query.filter_by(perfil_id=self.perfil_id, ativo=True).all():
            tela = Tela.query.filter_by(id=telacontrato.tela_id).one_or_none()
            if tela.nome == nome:
                return True
        return False

    def get_id(self):
        return self.id

    def alterar_email(self, email):
        self.email = email

    def set_active(self, ativo):
        self.ativo = ativo

    def ping(self):
        self.data_ultima_entrada = datetime.datetime.now()
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
        return self.ativo

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

    def alterar_atributos(self, form, empresa_id, new=False):
        self.nome = form.nome.data
        self.email = form.email.data
        self.empresa_id = empresa_id
        self.perfil_id = form.perfil.data
        self.ativo = form.ativo.data

        if new:
            self.data_assinatura = datetime.datetime.now()

    def ativar_desativar(self):
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True


    def retornar_telas_by_regras(self):
        telas = []
        for telaperfil in Telaperfil.query.filter_by(perfil_id=self.perfil_id, ativo=True).all():
            tela = Tela.query.filter_by(id=telaperfil.tela_id).one()
            telas.append(dict(nome=tela.nome, url=tela.url, icon=tela.icon))
        return telas


class Telaperfil(db.Model):
    """    Classe relacionamento entre Tela e Perfil    """
    __tablename__ = 'tela_perfil'
    id = db.Column(db.Integer(), primary_key=True)
    ativo = db.Column(db.Boolean, default=True)

    perfil_id = db.Column(db.Integer(), db.ForeignKey("perfil.id"), nullable=False)
    tela_id = db.Column(db.Integer(), db.ForeignKey("tela.id"), nullable=False)

    perfil = db.relationship("Perfil", back_populates="telaperfil")
    tela = db.relationship("Tela", back_populates="telaperfil")

    def __repr__(self) -> str:
        return f'<Telaperfil: {self.id}-{self.id}>'

    def salvar(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def alterar_atributos(self, form):
        self.perfil_id = form.perfil.data
        self.tela_id = form.tela.data

    def ativar_desativar(self):
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    @staticmethod
    def retornar_name_tela(id_):
        tela = Tela.query.filter_by(id=id_).first()
        return tela.get_name()

    @staticmethod
    def alterar_perfil(ativo: bool, *args):
        [[[Telaperfil.save_change(ativo, item) for item in posicao] for posicao in id_] for id_ in args]

    @staticmethod
    def save_change(ativo: bool, kwargs) -> None:
        telaperfil = Telaperfil.query.filter_by(perfil_id=kwargs['perfil_id'], tela_id=kwargs['tela_id']).one_or_none()

        if telaperfil:  # se exister a tela para o perfil
            if ativo:  # é para ativar
                if kwargs['perfil_nome'] == 'admin':  # o perfil é administrador
                    telaperfil.ativo = True
            else:  # o perfil não é administrador
                telaperfil.ativo = False  # desativa para qualquer perfil
        else:
            telaperfil = Telaperfil()
            telaperfil.perfil_id = kwargs['perfil_id']
            telaperfil.tela_id = kwargs['tela_id']
            if kwargs['perfil_nome'] == 'admin':  # o perfil é administrador
                telaperfil.ativo = True  # deixa ativa a tela
            else:  # o perfil não é administrador
                telaperfil.ativo = False  # deixa desativada a tela
        if telaperfil.salvar():
            flash("Tela do perfil não cadastrada", category="danger")
