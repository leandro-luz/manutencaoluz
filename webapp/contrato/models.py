from flask_login import current_user

from webapp import db
from webapp.empresa.models import Empresa
from webapp.utils.objetos import salvar


class Contrato(db.Model):
    """    Classe o Contrato de Assinaturas   """
    __tablename__ = 'contrato'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)

    empresa_gestora_id = db.Column(db.Integer(), nullable=True)

    empresa = db.relationship("Empresa", back_populates="contrato")
    telacontrato = db.relationship("Telacontrato", back_populates="contrato", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f'<Contrato: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        """ Função para alterar os atributos """
        self.nome = form.nome.data.upper()
        self.ativo = form.ativo.data
        self.empresa_gestora_id = current_user.empresa_id

    def ativar_desativar(self):
        """Função para ativar e desativar"""
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    @staticmethod
    def inativar_by_id(contrato_id):
        """Função que inativa o contrato pelo contrato_id"""
        contrato = Contrato.localizar_contrato_by_id(contrato_id)
        contrato.ativo = False
        salvar(contrato)

    @staticmethod
    def localizar_contrato_by_id(contrato_id):
        return Contrato.query.filter(Contrato.id == contrato_id,
                                     Contrato.empresa_gestora_id == current_user.empresa_id).one_or_none()


class Tela(db.Model):
    """    Classe das telas    """
    __tablename__ = 'tela'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    posicao = db.Column(db.Integer(), nullable=False)
    telacontrato = db.relationship("Telacontrato", back_populates="tela")
    telaperfilacesso = db.relationship("TelaPerfilAcesso", back_populates="tela")

    def __repr__(self) -> str:
        return f'<Tela: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        """    Altera os valores dos atributos da tela     """
        self.nome = form.nome.data.upper()
        self.icon = form.icon.data
        self.url = form.url.data
        self.posicao = form.posicao.data


class Telacontrato(db.Model):
    """    Classe Relacionando Telas e Planos    """
    __tablename__ = 'tela_contrato'
    id = db.Column(db.Integer(), primary_key=True)
    ativo = db.Column(db.Boolean, default=False)

    contrato_id = db.Column(db.Integer(), db.ForeignKey("contrato.id"), nullable=False)
    tela_id = db.Column(db.Integer(), db.ForeignKey("tela.id"), nullable=False)

    contrato = db.relationship("Contrato", back_populates="telacontrato")
    tela = db.relationship("Tela", back_populates="telacontrato")

    def __repr__(self):
        return f'<Telacontrato: {self.id}-{self.contrato_id}-{self.tela_id}>'

    def alterar_atributos(self, form, contrato_id) -> None:
        """    Altera os valores do contrato e tela    """
        self.contrato_id = contrato_id
        self.tela_id = form.tela.data

    @staticmethod
    def contagem_telas_ativas(contrato_id):
        return Telacontrato.query.filter_by(contrato_id=contrato_id).count()

    @staticmethod
    def verifica_empresas_vinculadas(contrato_id):
        """Função que verifica se o contrato não tem tela ativas e inativa as empresas vinculados"""
        # Caso não exista telas ativas para o contrato
        if Telacontrato.contagem_telas_ativas(contrato_id) == 0:
            # Inativa o contrato
            Contrato.inativar_by_id(contrato_id)
            # Busca as empresas vinculados ao contrato e inativa elas
            Empresa.inativar_by_contrato(contrato_id)
