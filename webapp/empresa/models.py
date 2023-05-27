import datetime
import logging
import re
from flask import flash
from itertools import cycle
from webapp import db


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class Interessado(db.Model):
    """    Classe de interessados no sistema    """
    id = db.Column(db.Integer(), primary_key=True)
    nome_fantasia = db.Column(db.String(50), nullable=False, unique=True)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=False)
    telefone = db.Column(db.String(20), nullable=False, unique=False)
    data_solicitacao = db.Column(db.DateTime(), nullable=True)
    data_cadastro = db.Column(db.DateTime(), nullable=True)

    def __repr__(self) -> str:
        return f'<Interessado {self.id}-{self.nome_fantasia}, {self.cnpj}, {self.email}>'

    def alterar_atributos(self, form) -> None:
        """    Função que alterar os atributos do objeto    """
        self.nome_fantasia = form.nome_fantasia.data
        self.cnpj = form.cnpj.data
        self.email = form.email.data
        self.telefone = form.telefone.data
        self.data_solicitacao = datetime.datetime.now()

    def salvar(self) -> bool:
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()} :{e}')
            db.session.rollback()
            return False

    def registrado(self) -> bool:
        """    Função para salvar a data de registro do 'lead' como cliente    """
        self.data_cadastro = datetime.datetime.now()
        return self.salvar()


class Tipoempresa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True, unique=True)
    empresa = db.relationship("Empresa", back_populates="tipoempresa")

    def __repr__(self) -> str:
        return f'<Tipoempresa: {self.id}-{self.nome}>'

    def salvar(self) -> bool:
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


class Empresa(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    razao_social = db.Column(db.String(100), nullable=False, index=True, unique=True)
    nome_fantasia = db.Column(db.String(100), nullable=True, unique=False)
    data_abertura = db.Column(db.DateTime(), nullable=True, unique=False)
    situacao = db.Column(db.String(50), nullable=True, unique=False)
    tipo = db.Column(db.String(20), nullable=True, unique=False)
    nome_responsavel = db.Column(db.String(50), nullable=True, unique=False)
    porte = db.Column(db.String(20), nullable=True, unique=False)
    natureza_juridica = db.Column(db.String(50), nullable=True, unique=False)
    cnae_principal = db.Column(db.String(10), nullable=True, unique=False)
    cnae_principal_texto = db.Column(db.String(200), nullable=True, unique=False)
    inscricao_estadual = db.Column(db.String(20), nullable=True, unique=False)
    inscricao_municipal = db.Column(db.String(20), nullable=True, unique=False)
    cep = db.Column(db.BigInteger(), nullable=False, unique=False)
    numero = db.Column(db.BigInteger(), nullable=False, unique=False)
    complemento = db.Column(db.String(50), nullable=False, unique=False)
    logradouro = db.Column(db.String(50), nullable=False, unique=False)
    bairro = db.Column(db.String(50), nullable=False, unique=False)
    municipio = db.Column(db.String(50), nullable=False, unique=False)
    uf = db.Column(db.String(3), nullable=False, unique=False)
    localizacao = db.Column(db.String(50), nullable=True, unique=False)
    telefone = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    ativo = db.Column(db.Boolean, default=False)
    data_cadastro = db.Column(db.DateTime(), nullable=True)
    empresa_gestora_id = db.Column(db.Integer(), nullable=False)

    contrato_id = db.Column(db.Integer(), db.ForeignKey("contrato.id"), nullable=False)
    tipoempresa_id = db.Column(db.Integer(), db.ForeignKey("tipoempresa.id"), nullable=False)

    contrato = db.relationship("Contrato", back_populates="empresa")
    tipoempresa = db.relationship("Tipoempresa", back_populates="empresa")
    usuario = db.relationship("Usuario", back_populates="empresa")
    perfil = db.relationship("Perfil", back_populates="empresa")
    equipamento = db.relationship("Equipamento", back_populates="empresa")
    supplier = db.relationship("Supplier", back_populates="empresa")

    def __repr__(self) -> str:
        return f'<Empresa: {self.id}-{self.nome_fantasia}>'

    def __init__(self, nome="") -> None:
        self.razao_social = nome

    def alterar_atributos_externo(self, form, empresa_id, tipoempresa_id, new=False) -> None:
        """    Alterações dos atributos da empresa     """
        self.nome_fantasia = form.nome_fantasia.data
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
        self.contrato_id = form.contrato.data
        self.empresa_gestora_id = empresa_id
        self.tipoempresa_id = tipoempresa_id
        if new:
            self.data_cadastro = datetime.datetime.now()

    def alterar_atributos(self, form, empresa_id, tipoempresa_id, new=False) -> None:
        self.alterar_atributos_externo(form, empresa_id, tipoempresa_id, new)
        self.razao_social = form.razao_social.data
        self.data_abertura = form.data_abertura.data
        self.situacao = form.situacao.data
        self.tipo = form.tipo.data
        self.nome_responsavel = form.nome_responsavel.data
        self.porte = form.porte.data
        self.natureza_juridica = form.natureza_juridica.data
        self.cnae_principal = form.cnae_principal.data
        self.cnae_principal_texto = form.cnae_principal_texto.data
        self.inscricao_estadual = form.inscricao_estadual.data
        self.inscricao_municipal = form.inscricao_municipal.data
        self.localizacao = form.localizacao.data
        self.ativo = form.ativo.data

    def ativar_desativar(self) -> None:
        """    Altera em ativo e inativo a empresa    """
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    def salvar(self):
        """    Função para salvar no banco de dados o objeto    """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

    def importar_interessado(self, interessado: [Interessado]) -> None:
        self.nome_fantasia = interessado.nome_fantasia
        self.cnpj = interessado.cnpj
        self.email = interessado.email
        self.telefone = interessado.telefone

    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
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
    def listar_empresas_by_plano(value):
        """    Função que retorna uma lista de empresas com base no identificador    """
        return Empresa.query.filter_by(contrato_id=value).all()
