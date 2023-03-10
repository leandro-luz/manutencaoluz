import logging
from webapp import db
from flask import flash

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Plan(db.Model):
    """    Classe o Plano de Assinaturas   """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company = db.relationship("Company", back_populates="plan")
    viewplan = db.relationship("ViewPlan", back_populates="plan")

    def __repr__(self) -> str:
        return f'<Plan: {self.id}-{self.name}>'

    def change_attributes(self, form) -> None:
        self.name = form.name.data

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

class View(db.Model):
    """    Classe das telas    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    viewplan = db.relationship("ViewPlan", back_populates="view")
    viewrole = db.relationship("ViewRole", back_populates="view")

    def __repr__(self) -> str:
        return f'<View: {self.id}-{self.name}>'

    def change_attributes(self, form) -> None:
        """    Altera os valores dos atributos da tela     """
        self.name = form.name.data
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


class ViewPlan(db.Model):
    """    Classe Relacionando Telas e Planos    """
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=False)

    plan_id = db.Column(db.Integer(), db.ForeignKey("plan.id"))
    plan = db.relationship("Plan", back_populates="viewplan")
    view_id = db.Column(db.Integer(), db.ForeignKey("view.id"))
    view = db.relationship("View", back_populates="viewplan")

    def __repr__(self):
        return f'<ViewPlan: {self.id}-{self.id}>'

    def change_attributes(self, form) -> None:
        """    Altera os valores do plano e tela    """
        self.plan_id = form.plan.data
        self.view_id = form.view.data

    def change_active(self) -> None:
        """    Altera em ativo e inativo a tela do plano de assinatura    """
        if self.active:
            self.active = False
            flash("Plano desativado com sucesso", category="success")
        else:
            self.active = True
            flash("Plano ativado com sucesso", category="success")

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no bando de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False
