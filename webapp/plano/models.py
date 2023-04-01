import logging
from webapp import db
from flask import flash

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Plano(db.Model):
    """    Classe o Plano de Assinaturas   """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    empresa = db.relationship("Empresa", back_populates="plano")
    telaplano = db.relationship("Telaplano", back_populates="plano")

    def __repr__(self) -> str:
        return f'<Plano: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        self.nome = form.nome.data

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

class Tela(db.Model):
    """    Classe das telas    """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    telaplano = db.relationship("Telaplano", back_populates="tela")
    viewrole = db.relationship("ViewRole", back_populates="tela")

    def __repr__(self) -> str:
        return f'<Tela: {self.id}-{self.nome}>'

    def alterar_atributos(self, form) -> None:
        """    Altera os valores dos atributos da tela     """
        self.nome = form.nome.data
        self.icon = form.icon.data
        self.url = form.url.data

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


class Telaplano(db.Model):
    """    Classe Relacionando Telas e Planos    """
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=False)

    plano_id = db.Column(db.Integer(), db.ForeignKey("plano.id"), nullable=False)
    tela_id = db.Column(db.Integer(), db.ForeignKey("tela.id"), nullable=False)

    plano = db.relationship("Plano", back_populates="telaplano")
    tela = db.relationship("Tela", back_populates="telaplano")

    def __repr__(self):
        return f'<Telaplano: {self.id}-{self.id}>'

    def alterar_atributos(self, form) -> None:
        """    Altera os valores do plano e tela    """
        self.plano_id = form.plano.data
        self.tela_id = form.view.data

    def change_active(self) -> None:
        """    Altera em ativo e inativo a tela do plano de assinatura    """
        if self.active:
            self.active = False
            flash("Plano desativado com sucesso", category="success")
        else:
            self.active = True
            flash("Plano ativado com sucesso", category="success")

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
