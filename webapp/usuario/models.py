import datetime
import config
import logging
import string
import random
from flask import flash
from webapp.usuario import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from webapp.empresa.models import Empresa
from webapp.contrato.models import Tela, Telacontrato
from flask_login import current_user
from flask_jwt_extended import create_access_token, get_jwt_identity
from webapp.utils.tools import password_random

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class PerfilAcesso(db.Model):
    """    Classe do perfil de acesso    """

    # nome do arquivo para cadastro em lote
    nome_doc = 'padrão_perfil_acesso'
    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Descrição': 'descricao', 'Ativo': 'ativo'}

    __tablename__ = 'perfil_acesso'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), unique=False, index=True)
    descricao = db.Column(db.String(50))
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="perfilacesso")
    empresa = db.relationship("Empresa", back_populates="perfilacesso")
    telaperfilacesso = db.relationship("TelaPerfilAcesso", back_populates="perfilacesso")

    def __repr__(self) -> str:
        return f'<PerfilAcesso: {self.id}-{self.nome}>'

    def ativar_desativar(self):
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def alterar_atributos(self, form, empresa_id):
        self.nome = form.nome.data.upper()
        self.descricao = form.descricao.data.upper()
        self.empresa_id = empresa_id

    @staticmethod
    def inativar_by_id(perfilacesso_id):
        perfilacesso = PerfilAcesso.query.filter_by(id=perfilacesso_id).one_or_none()
        perfilacesso.ativo = False
        perfilacesso.salvar()

    @staticmethod
    def listar_regras_by_empresa(empresa_id: int):
        return PerfilAcesso.query.filter_by(empresa_id=empresa_id).all()


class PerfilManutentor(db.Model):
    """    Classe do perfil de acesso    """

    __tablename__ = 'perfil_manutentor'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), unique=False, index=True)

    tiposituacaoordemperfilmanutentor = db.relationship("TipoSituacaoOrdemPerfilManutentor",
                                                        back_populates="perfilmanutentor")
    perfilmanutentorusuario = db.relationship("PerfilManutentorUsuario", back_populates="perfilmanutentor")

    def __repr__(self) -> str:
        return f'<PerfilManutentor: {self.id}-{self.nome}>'


class PerfilManutentorUsuario(db.Model):
    """    Classe relacionamento entre Tela e PerfilAcesso    """
    __tablename__ = 'perfil_manutentor_usuario'
    id = db.Column(db.Integer(), primary_key=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    perfilmanutentor_id = db.Column(db.Integer(), db.ForeignKey("perfil_manutentor.id"), nullable=False)
    usuario_id = db.Column(db.Integer(), db.ForeignKey("usuario.id"), nullable=False)

    perfilmanutentor = db.relationship("PerfilManutentor", back_populates="perfilmanutentorusuario")
    usuario = db.relationship("Usuario", back_populates="perfilmanutentorusuario")

    def __repr__(self) -> str:
        return f'<PerfilManutentorUsuario: {self.id}-{self.perfilmanutentor_id}-{self.usuario_id}>'

    def alterar_atributos(self, form, usuario_id):
        self.perfilmanutentor_id = form.perfilmanutentor.data
        self.usuario_id = usuario_id

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

    def ativar_desativar(self):
        """Função para ativar e desativar"""
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True


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
        # self.contador_acesso_temporario = 0
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
    """ Classe de usuário    """
    # nome do arquivo para cadastro em lote
    nome_doc = 'padrão_usuarios'
    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Email*': 'email', 'PerfilAcesso*': 'perfilacesso_id'}

    __tablename__ = 'usuario'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=False)
    data_assinatura = db.Column(db.DateTime(), nullable=True)
    data_ultima_entrada = db.Column(db.DateTime(), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    perfilacesso_id = db.Column(db.Integer(), db.ForeignKey("perfil_acesso.id"), nullable=False)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)
    senha_id = db.Column(db.Integer(), db.ForeignKey("senha.id"), nullable=False)

    perfilacesso = db.relationship("PerfilAcesso", back_populates="usuario")
    empresa = db.relationship("Empresa", back_populates="usuario")
    senha = db.relationship("Senha", back_populates="usuario")
    ordemservico = db.relationship("OrdemServico", back_populates="usuario")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="usuario")
    perfilmanutentorusuario = db.relationship("PerfilManutentorUsuario", back_populates="usuario")

    def __repr__(self):
        return f'<Usuario: {self.id}-{self.nome}>'

    def usuario_administrador(self, nome: str, email: str, empresa_id: int, perfilacesso_id: int,
                              senha_id: int) -> None:
        """    Função para cadastrar as informações de administrador     """
        self.nome = nome.upper()
        self.email = email.upper()
        self.senha_id = senha_id
        self.empresa_id = empresa_id
        self.perfilacesso_id = perfilacesso_id
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

    @staticmethod
    def salvar_lote(lote):
        try:
            db.session.add_all(lote)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar ao tentar salvar o lote:{e}')
            db.session.rollback()
        return False

    # # @cache.memoize(60)
    def tela_permitida(self, nome: str) -> bool:
        """
        Verifica se a tela está cadastrada para o perfil e se está ativo
        """
        for telacontrato in TelaPerfilAcesso.query.filter_by(perfilacesso_id=self.perfilacesso_id).all():
            tela = Tela.query.filter_by(id=telacontrato.tela_id).one_or_none()
            if tela.nome == nome:
                return True
        return False

    def get_id(self):
        return self.id

    def alterar_email(self, email):
        self.email = email.upper()

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
        self.nome = form.nome.data.upper()
        self.email = form.email.data.upper()
        self.empresa_id = empresa_id
        self.perfilacesso_id = form.perfilacesso.data
        self.ativo = form.ativo.data

        if new:
            self.data_assinatura = datetime.datetime.now()

    def ativar_desativar(self):
        """Função para ativar e desativar"""
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    def retornar_telas_by_regras(self):
        """Função retorna as telas permitidas ao usuário em ordem"""
        telas = []
        lista_telas = Tela.query.filter(Tela.id == TelaPerfilAcesso.tela_id,
                                        # TelaPerfilAcesso.ativo == True,
                                        TelaPerfilAcesso.perfilacesso_id == self.perfilacesso_id).order_by(
            Tela.posicao.asc())
        telas = [{'nome': tela.nome, 'url': tela.url, 'icon': tela.icon} for tela in lista_telas]
        return telas

    @staticmethod
    def verifica_perfil_manutentor(perfil_nome):
        """Função que verifica se o usuário tem o perfil de manutentor e está ativo"""
        resultado = False
        if PerfilManutentor.query.filter(
                PerfilManutentor.nome == perfil_nome,
                PerfilManutentorUsuario.perfilmanutentor_id == PerfilManutentor.id,
                PerfilManutentorUsuario.ativo == True,
                Usuario.id == PerfilManutentorUsuario.usuario_id,
                Usuario.id == current_user.id
        ).one_or_none():
            resultado = True

        return resultado

    @staticmethod
    def verifica_usuario_acesso_tela(tela_nome):
        """Função que verifica se o usuário tem perfil de acesso e está ativo"""
        resultado = False
        if TelaPerfilAcesso.query.filter(
                # TelaPerfilAcesso.ativo == True,
                TelaPerfilAcesso.tela_id == Tela.id,
                Tela.nome == tela_nome,
                Usuario.perfilacesso_id == TelaPerfilAcesso.perfilacesso_id,
                Usuario.id == current_user.id
        ).one_or_none():
            resultado = True

        return resultado

    @staticmethod
    def inativar_by_perfilacesso(perfilacesso_id):
        """Função que inativa os usuarios vinculados a um perfilacesso"""
        # Busca os usuarios vinculados ao perfilacesso
        usuarios = Usuario.query.filter_by(perfilacesso_id=perfilacesso_id).all()
        if usuarios:
            # Inativa o usuário
            for usuario in usuarios:
                usuario.ativo = False
                usuario.salvar()


class TelaPerfilAcesso(db.Model):
    """    Classe relacionamento entre Tela e PerfilAcesso    """
    __tablename__ = 'tela_perfil_acesso'
    id = db.Column(db.Integer(), primary_key=True)

    perfilacesso_id = db.Column(db.Integer(), db.ForeignKey("perfil_acesso.id"), nullable=False)
    tela_id = db.Column(db.Integer(), db.ForeignKey("tela.id"), nullable=False)

    perfilacesso = db.relationship("PerfilAcesso", back_populates="telaperfilacesso")
    tela = db.relationship("Tela", back_populates="telaperfilacesso")

    def __repr__(self) -> str:
        return f'<TelaPerfilAcesso: {self.id}-{self.perfilacesso_id}-{self.tela_id}>'

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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def alterar_atributos(self, form, perfilacesso_id):
        self.perfilacesso_id = perfilacesso_id
        self.tela_id = form.tela.data

    def ativar_desativar(self):
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    @staticmethod
    def excluir_by_id(telaperfilacesso_id):
        """Função que inativa uma telaperfilacesso pelo id"""
        telaperfilacesso = TelaPerfilAcesso.query.filter_by(id=telaperfilacesso_id).one_or_none()
        telaperfilacesso.excluir()

    @staticmethod
    def retornar_name_tela(id_):
        tela = Tela.query.filter_by(id=id_).first()
        return tela.get_name()

    @staticmethod
    def alterar_perfil(ativo: bool, *args):
        [[[TelaPerfilAcesso.save_change(ativo, item) for item in posicao] for posicao in id_] for id_ in args]

    @staticmethod
    def save_change(ativo: bool, kwargs) -> None:
        telaperfilacesso = TelaPerfilAcesso.query.filter_by(perfilacesso_id=kwargs['perfilacesso_id'],
                                                            tela_id=kwargs['tela_id']).one_or_none()

        if telaperfilacesso:  # se exister a tela para o perfil
            if ativo:  # é para ativar
                if kwargs['perfil_nome'] == 'admin':  # o perfil é administrador
                    telaperfilacesso.ativo = True
            else:  # o perfil não é administrador
                telaperfilacesso.ativo = False  # desativa para qualquer perfil
        else:
            telaperfilacesso = TelaPerfilAcesso()
            telaperfilacesso.perfilacesso_id = kwargs['perfilacesso_id']
            telaperfilacesso.tela_id = kwargs['tela_id']
            if kwargs['perfil_nome'] == 'admin':  # o perfil é administrador
                telaperfilacesso.ativo = True  # deixa ativa a tela
            else:  # o perfil não é administrador
                telaperfilacesso.ativo = False  # deixa desativada a tela
        if telaperfilacesso.salvar():
            flash("Tela do perfil não cadastrada", category="danger")

    @staticmethod
    def contagem_telas_ativas(perfilacesso_id):
        return TelaPerfilAcesso.query.filter_by(perfilacesso_id=perfilacesso_id).count()

    @staticmethod
    def verifica_usuarios_vinculados(perfilacesso_id):
        """Função que verifica se o perfil não tem tela ativas e inativa os usuarios vinculados"""
        # Caso não exista telas ativas para o perfil
        if TelaPerfilAcesso.contagem_telas_ativas(perfilacesso_id) == 0:
            # Inativa o perfilacesso
            PerfilAcesso.inativar_by_id(perfilacesso_id)
            # Busca os usuarios vinculados ao perfilacesso e inativa eles
            Usuario.inativar_by_perfilacesso(perfilacesso_id)

    @staticmethod
    def inativar_by_contrato(tela_id, contrato_id):
        """Função que inativa os perfisacesso e usuários que estiverem vinculados a tela e contrato"""

        # Localiza as telas vinculadas a um perfilacesso vinculados a um contrato
        telasperfilacesso = TelaPerfilAcesso.query.filter(
            TelaPerfilAcesso.tela_id == tela_id,
            TelaPerfilAcesso.perfilacesso_id == PerfilAcesso.id,
            PerfilAcesso.empresa_id == Empresa.id,
            Empresa.contrato_id == contrato_id).all()

        for telaperfilacesso in telasperfilacesso:
            # Inativa todas as telas encontradas
            telaperfilacesso.excluir_by_id(telaperfilacesso.id)
            # Verifica se o perfilacesso está sem telas ativas
            TelaPerfilAcesso.verifica_usuarios_vinculados(telaperfilacesso.perfilacesso_id)
