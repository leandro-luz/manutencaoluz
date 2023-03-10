import datetime
import logging
import re
from flask import flash
from itertools import cycle
from webapp import db


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
        """    Função que grava as informações repassadas pelo formulário    """
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
    """    Classe de interessados no sistema    """
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
        """    Função que alterar os atributos do objeto    """
        self.name = form.name.data
        self.cnpj = form.cnpj.data
        self.email = form.email.data
        self.telefone = form.telefone.data
        self.data_solicitacao = datetime.datetime.now()

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()} :{e}')
            db.session.rollback()
            flash("Erro ao cadastrar o lead no banco de dados", category="danger")
            return False

    def registred(self) -> bool:
        """    Função para salvar a data de registro do 'lead' como cliente    """
        self.data_cadastro = datetime.datetime.now()
        return self.save()


class Companytype(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    company = db.relationship("Company", back_populates="companytype")

    def __repr__(self) -> str:
        return f'<Companytype: {self.id}-{self.name}>'

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            flash("Erro ao cadastrar/atualizar o tipo de empresa no banco de dados", category="danger")
            return False


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
    subbusiness_id = db.Column(db.Integer(), db.ForeignKey("subbusiness.id"), nullable=False)
    subbusiness = db.relationship("Subbusiness", back_populates="company")
    plan_id = db.Column(db.Integer(), db.ForeignKey("plan.id"), nullable=False)
    plan = db.relationship("Plan", back_populates="company")
    companytype_id = db.Column(db.Integer(), db.ForeignKey("companytype.id"), nullable=False)
    companytype = db.relationship("Companytype", back_populates="company")

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
        """    Alterações dos atributos da empresa     """
        self.name = form.name.data
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

    def import_lead(self, lead: [Lead]) -> None:
        self.name = lead.name
        self.cnpj = lead.cnpj
        self.email = lead.email
        self.telefone = lead.telefone

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        length_cnpj = 14

        # deixado somente os números do cnpj
        cnpj = "".join(re.findall("\d+", cnpj))

        # verifica se a quantidade de caracteres estão no limite
        if len(cnpj) != length_cnpj:
            return False

        # verifica se existe somente números
        if cnpj in (c * length_cnpj for c in "1234567890"):
            return False

        # realiza a validação do cnpj
        cnpj_r = cnpj[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                return False

        return True

    @staticmethod
    def list_companies_by_plan(value):
        """    Função que retorna uma lista de empresas com base no identificador    """
        return Company.query.filter_by(plan_id=value).all()
