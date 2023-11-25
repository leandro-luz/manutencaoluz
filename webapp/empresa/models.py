import re
from itertools import cycle

from flask_login import current_user

from webapp import db
from webapp.utils.objetos import atributo_existe
from webapp.utils.objetos import salvar
from webapp.utils.tools import data_atual_utc


class Interessado(db.Model):
    """    Classe de interessados no sistema    """
    __tablename__ = 'interessado'
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
        self.nome_fantasia = form.nome_fantasia.data.upper()
        self.cnpj = form.cnpj.data
        self.email = form.email.data.upper()
        self.telefone = form.telefone.data
        self.data_solicitacao = data_atual_utc()

    def registrado(self) -> bool:
        """    Função para salvar a data de registro do 'lead' como cliente    """
        self.data_cadastro = data_atual_utc()
        return salvar(self)


class Tipoempresa(db.Model):
    __tablename__ = 'tipo_empresa'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True, unique=True)
    empresa = db.relationship("Empresa", back_populates="tipoempresa")

    def __repr__(self) -> str:
        return f'<Tipoempresa: {self.id}-{self.nome}>'


class Empresa(db.Model):
    """  Classe da empresa   """
    # titulos para cadastro
    titulos_doc = {'CNPJ*': 'cnpj', 'Razao_Social*': 'razao_social', 'Nome_Fantasia*': 'nome_fantasia',
                   'Tipo*': 'tipo', 'CEP*': 'cep', 'Logradouro*': 'logradouro', 'Numero*': 'numero',
                   'Bairro*': 'bairro', 'Municipio*': 'municipio', 'UF*': 'uf',
                   'Email*': 'email', 'Telefone*': 'telefone', 'Contrato*': 'contrato_id',
                   'Situacao': 'situacao', 'Porte': 'porte', 'Data_Abertura': 'data_abertura',
                   'Natureza_Juridica': 'natureza_juridica',
                   'CNAE_P_Codigo': 'cnae_principal', 'CNAE_P_Texto': 'cnae_principal_texto',
                   'Inscricao_Estadual': 'inscricao_estadual', 'Inscricao_Municipal': 'inscricao_municipal',
                   'Localizacao': 'localizacao', 'Complemento': 'complemento', 'Nome_Responsavel': 'nome_responsavel'
                   }

    titulos_valor = {'CNPJ*': 'cnpj', 'Razao_Social*': 'razao_social', 'Nome_Fantasia*': 'nome_fantasia',
                     'Tipo*': 'tipo', 'CEP*': 'cep', 'Logradouro*': 'logradouro', 'Numero*': 'numero',
                     'Bairro*': 'bairro', 'Municipio*': 'municipio', 'UF*': 'uf',
                     'Email*': 'email', 'Telefone*': 'telefone', 'Contrato*': 'contrato_id',
                     'Situacao': 'situacao', 'Porte': 'porte',
                     'Natureza_Juridica': 'natureza_juridica',
                     'CNAE_P_Codigo': 'cnae_principal', 'CNAE_P_Texto': 'cnae_principal_texto',
                     'Inscricao_Estadual': 'inscricao_estadual', 'Inscricao_Municipal': 'inscricao_municipal',
                     'Localizacao': 'localizacao', 'Complemento': 'complemento', 'Nome_Responsavel': 'nome_responsavel'
                     }

    titulos_data = {'Data_Abertura': 'data_abertura'}

    titulos_csv = {'cnpj; razao_social; nome_fantasia; data_abertura; situacao; tipo; '
                   + 'nome_responsavel; porte; natureza_juridica; cnae_principal; cnae_principal_texto; '
                   + 'inscricao_estadual; inscricao_municipal; cep; numero; complemento; logradouro; bairro; '
                   + 'municipio; uf; latitude; telefone; email; ativo; data_cadastro; contrato_nome'}

    __tablename__ = 'empresa'
    id = db.Column(db.Integer(), primary_key=True)
    cnpj = db.Column(db.String(18), nullable=False, unique=False)
    razao_social = db.Column(db.String(100), nullable=False, index=True, unique=False)
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
    cep = db.Column(db.String(10), nullable=False, unique=False)
    numero = db.Column(db.BigInteger(), nullable=False, unique=False)
    complemento = db.Column(db.String(50), nullable=True, unique=False)
    logradouro = db.Column(db.String(50), nullable=False, unique=False)
    bairro = db.Column(db.String(50), nullable=False, unique=False)
    municipio = db.Column(db.String(50), nullable=False, unique=False)
    uf = db.Column(db.String(3), nullable=False, unique=False)
    latitude = db.Column(db.String(20), nullable=True)
    telefone = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=False)
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime(), nullable=True)
    empresa_gestora_id = db.Column(db.Integer(), nullable=False, default=1)

    contrato_id = db.Column(db.Integer(), db.ForeignKey("contrato.id"), nullable=False)
    tipoempresa_id = db.Column(db.Integer(), db.ForeignKey("tipo_empresa.id"), nullable=False)

    contrato = db.relationship("Contrato", back_populates="empresa")
    tipoempresa = db.relationship("Tipoempresa", back_populates="empresa")
    usuario = db.relationship("Usuario", back_populates="empresa", cascade="all, delete-orphan")
    perfilacesso = db.relationship("PerfilAcesso", back_populates="empresa", cascade="all, delete-orphan")
    grupo = db.relationship("Grupo", back_populates="empresa", cascade="all, delete-orphan")
    pavimento = db.relationship("Pavimento", back_populates="empresa", cascade="all, delete-orphan")
    setor = db.relationship("Setor", back_populates="empresa", cascade="all, delete-orphan")
    local = db.relationship("Local", back_populates="empresa", cascade="all, delete-orphan")

    supplier = db.relationship("Supplier", back_populates="empresa")

    def __repr__(self) -> str:
        return f'{self.cnpj}; {self.razao_social}; {self.nome_fantasia}; {self.data_abertura}; ' \
               f'{self.situacao}; {self.tipo}; {self.nome_responsavel}; {self.porte}; {self.natureza_juridica}; ' \
               f'{self.cnae_principal}; {self.cnae_principal_texto}; {self.inscricao_estadual}; ' \
               f'{self.inscricao_municipal}; {self.cep}; {self.numero}; {self.complemento}; {self.logradouro}; ' \
               f'{self.bairro}; {self.municipio}; {self.uf}; {self.latitude}; {self.telefone}; {self.email}; ' \
               f'{self.ativo}; {self.data_cadastro}; {atributo_existe(self, "contrato", "nome")}'

    def alterar_atributos_externo(self, form, empresa_id, tipoempresa_id, new=False) -> None:
        """    Alterações dos atributos da empresa     """
        self.nome_fantasia = form.nome_fantasia.data.upper()
        self.razao_social = form.razao_social.data.upper()
        self.cnpj = form.cnpj.data
        self.cep = form.cep.data
        self.logradouro = form.logradouro.data.upper()
        self.bairro = form.bairro.data.upper()
        self.municipio = form.municipio.data.upper()
        self.uf = form.uf.data.upper()
        self.numero = form.numero.data
        self.complemento = form.complemento.data.upper()
        self.email = form.email.data.upper()
        self.telefone = form.telefone.data
        self.contrato_id = form.contrato.data
        self.empresa_gestora_id = empresa_id
        self.tipoempresa_id = tipoempresa_id
        if new:
            self.data_cadastro = data_atual_utc()

    def alterar_atributos(self, form, empresa_id, tipoempresa_id, new=False) -> None:
        """Função para alterar os atributos"""
        self.alterar_atributos_externo(form, empresa_id, tipoempresa_id, new)
        self.razao_social = form.razao_social.data.upper()
        self.data_abertura = form.data_abertura.data
        self.situacao = form.situacao.data.upper()
        self.tipo = form.tipo.data.upper()
        self.nome_responsavel = form.nome_responsavel.data.upper()
        self.porte = form.porte.data.upper()
        self.natureza_juridica = form.natureza_juridica.data.upper()
        self.cnae_principal = form.cnae_principal.data.upper()
        self.cnae_principal_texto = form.cnae_principal_texto.data.upper()
        self.inscricao_estadual = form.inscricao_estadual.data.upper()
        self.inscricao_municipal = form.inscricao_municipal.data.upper()
        self.ativo = form.ativo.data

    def ativar_desativar(self) -> None:
        """    Altera em ativo e inativo a empresa    """
        if self.ativo:
            self.ativo = False
        else:
            self.ativo = True

    def importar_interessado(self, interessado: [Interessado]) -> None:
        """Função para importar as informações do interessado"""
        self.nome_fantasia = interessado.nome_fantasia.upper()
        self.cnpj = interessado.cnpj
        self.email = interessado.email.upper()
        self.telefone = interessado.telefone

    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Função para validar o cnpj"""
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

    @staticmethod
    def inativar_by_contrato(contrato_id):
        """Função que inativa os empresas vinculadas a um contrato"""
        # Busca as empresas vinculados ao contrato
        empresas = Empresa.query.filter_by(contrato_id=contrato_id).all()
        if empresas:
            # Inativa a empresa
            for empresa in empresas:
                empresa.ativo = False
                salvar(empresa)

    @staticmethod
    def localizar_empresa_by_id(id):
        """Função que localiza uma empresa pelo seu id que esteja vinculada a empresa do usuário"""
        return Empresa.query.filter(Empresa.id == id,
                                    Empresa.empresa_gestora_id == current_user.empresa_id).one_or_none()

    @staticmethod
    def lista_clientes(id):
        """Função que retorna a lista de outras empresas vinculadas a uma empresa"""
        clientes = Empresa.query.filter(
            Empresa.id != 1,
            Empresa.empresa_gestora_id == id).all()
        return [{cliente.nome_fantasia: Empresa.lista_clientes(cliente.id)} for cliente in clientes]
