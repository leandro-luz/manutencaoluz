import datetime
import logging
from webapp import db
from flask import flash

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Business(db.Model):
    """    Classe de Negócio    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    subbusiness = db.relationship("Subbusiness", back_populates="business")

    def __repr__(self) -> str:
        return f'<Business: {self.id}-{self.name}>'

    def change_attributes(self, form) -> None:
        """    Função para alteração dos atributos do Negócio    """
        self.name = form.name.data

    def save(self) -> None:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            flash("Erro ao cadastrar/atualizar o negócio no banco de dados", category="success")


class Subbusiness(db.Model):
    """    Classe de subnegócios    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=False)
    business_id = db.Column(db.Integer(), db.ForeignKey("business.id"))
    business = db.relationship("Business", back_populates="subbusiness")
    company = db.relationship("Company", back_populates="subbusiness")

    def __repr__(self) -> str:
        return f'<SubBusiness: {self.id}-{self.name}>'

    def change_attributes(self, form) -> None:
        """    Função que grava as informaçõe repassadas pelo formulário    """
        self.name = form.name.data
        self.business_id = form.business.data

    def save(self) -> None:
        """    Função que salva as informações no banco de dados    """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            flash("Erro ao cadastrar/atualizar o subnegócios no banco de dados", category="success")


class Lead(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=False)
    telefone = db.Column(db.String(20), nullable=False, unique=False)
    data_solicitacao = db.Column(db.DateTime(), nullable=True)
    data_cadastro = db.Column(db.DateTime(), nullable=True)

    def __repr__(self) -> str:
        return f'<Lead {self.name}, {self.cnpj}, {self.email}>'

    def change_attributes(self, form) -> None:
        self.name = form.name.data
        self.cnpj = form.cnpj.data
        self.email = form.email.data
        self.telefone = form.telefone.data
        self.data_solicitacao = datetime.datetime.now()

    def save(self) -> bool:
        try:
            db.session.add(self)
            db.session.commit()
            flash("Informações enviadas com sucesso, em breve vamos lhe atender", category="success")
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()} :{e}')
            db.session.rollback()
            flash("Erro ao cadastrar o lead no banco de dados", category="danger")
            return False

    def registred(self):
        """    Função para salvar a data de registro do led como cliente    """
        self.data_cadastro = datetime.datetime.now()
        self.save()

class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    cep = db.Column(db.BigInteger(), nullable=False, unique=False)

    numero = db.Column(db.BigInteger(), nullable=False, unique=False)
    complemento = db.Column(db.String(50), nullable=False, unique=False)
    logradouro = db.Column(db.String(50), nullable=False, unique=False)
    bairro = db.Column(db.String(50), nullable=False, unique=False)
    municipio = db.Column(db.String(50), nullable=False, unique=False)
    uf = db.Column(db.String(3), nullable=False, unique=False)
    telefone = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    manager_company_id = db.Column(db.Integer(), nullable=False)
    subbusiness_id = db.Column(db.Integer(), db.ForeignKey("subbusiness.id"))
    subbusiness = db.relationship("Subbusiness", back_populates="company")
    plan_id = db.Column(db.Integer(), db.ForeignKey("plan.id"))
    plan = db.relationship("Plan", back_populates="company")

    user = db.relationship("User", back_populates="company")
    role = db.relationship("Role", back_populates="company")
    asset = db.relationship("Asset", back_populates="company")
    # group = db.relationship("Group", back_populates="company")
    supplier = db.relationship("Supplier", back_populates="company")

    def __repr__(self) -> str:
        return f'<Company: {self.id}-{self.name}>'

    def __init__(self, name="") -> None:
        self.business_id = Subbusiness.query.filter_by(name="teste").one()
        self.name = name

    def change_attributes(self, form, company_id, new=False) -> None:
        """    Alteraçãos dos atributos da empresa     """
        self.name = form.name.data
        # numero = int("".join(re.findall("\d+", form.cnpj.data)))  # deixado somente os numeros do cnpj
        self.cnpj = form.cnpj.data
        self.cep = form.cep.data
        self.logradouro = form.logradouro.data
        self.bairro = form.bairro.data
        self.municipio = form.municipio.data
        self.uf = form.uf.data
        self.numero = form.numero.data
        self.complemento = form.complemento.data
        self.email = form.email.data
        self.telefone = form.telefone.data
        self.active = form.active.data
        self.subbusiness_id = form.subbusiness.data
        self.plan_id = form.plan.data
        self.manager_company_id = company_id
        if new:
            self.member_since = datetime.datetime.now()

    def change_active(self) -> None:
        """    Altera em ativo e inativo a empresa    """
        if self.active:
            self.active = False
            flash("Empresa desativada com sucesso", category="success")
        else:
            self.active = True
            flash("Empresa ativada com sucesso", category="success")

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            flash("Erro ao cadastrar/atualizar a empresa no banco de dados", category="danger")
            return False

    def import_lead(self, lead:[Lead]) -> None:
        self.name = lead.name
        self.cnpj = lead.cnpj
        self.email = lead.email
        self.telefone = lead.telefone



    @staticmethod
    def list_companies_by_plan(value):
        """    Função que retorna uma lista de empresas com base no indentificador    """
        return Company.query.filter_by(plan_id=value).all()
