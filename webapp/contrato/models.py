import logging
from webapp import db
from flask import flash

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Contrato(db.Model):
    """    Classe o Contrato de Assinaturas   """
    __tablename__ = 'contrato'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True )
    empresa = db.relationship("Empresa", back_populates="contrato")
    telacontrato = db.relationship("Telacontrato", back_populates="contrato")

    def __repr__(self) -> str:
        return f'<Contrato: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        self.nome = form.nome.data

    def salvar(self, new, form) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()

            if new:
            #     # cadastrar todas as telas para o novo contrato
                new_contrato = Contrato.query.filter_by(nome=form.nome.data).one_or_none()
                telascontrato = [Telacontrato(tela_id=tela.id, contrato_id=new_contrato.id, ativo=False)
                                 for tela in Tela.query.all()]
                db.session.add_all(telascontrato)
                db.session.commit()

            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

class Tela(db.Model):
    """    Classe das telas    """
    __tablename__ = 'tela'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    telacontrato = db.relationship("Telacontrato", back_populates="tela")
    telaperfil = db.relationship("Telaperfil", back_populates="tela")

    def __repr__(self) -> str:
        return f'<Tela: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        """    Altera os valores dos atributos da tela     """
        self.nome = form.nome.data
        self.icon = form.icon.data
        self.url = form.url.data

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

    def alterar_atributos(self, form) -> None:
        """    Altera os valores do contrato e tela    """
        self.contrato_id = form.contrato.data
        self.tela_id = form.tela.data

    def ativar_desativar(self) -> None:
        """    Altera em ativo e inativo a tela do contrato de assinatura    """
        if self.ativo:
            self.ativo = False
            flash("Contrato desativado com sucesso", category="success")
        else:
            self.ativo = True
            flash("Contrato ativado com sucesso", category="success")

    def salvar(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no bando de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False
