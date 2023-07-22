import logging
from webapp import db
from flask_login import current_user

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class Grupo(db.Model):
    """    Classe de grupo de ativos    """

    nome_doc = 'padrão_grupo'
    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome'}

    __tablename__ = 'grupo'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="grupo")
    subgrupo = db.relationship("Subgrupo", back_populates="grupo")

    def __repr__(self):
        return f'<Grupo: {self.id}-{self.nome}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
        self.ativo = form.ativo.data
        self.empresa_id = current_user.empresa_id

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


class Subgrupo(db.Model):
    """    Classe de sistemas nos ativos   """

    nome_doc = 'padrão_subgrupo'
    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Grupo*': 'grupo'}

    __tablename__ = 'subgrupo'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    grupo_id = db.Column(db.Integer(), db.ForeignKey("grupo.id"), nullable=True)

    grupo = db.relationship("Grupo", back_populates="subgrupo")
    equipamento = db.relationship("Equipamento", back_populates="subgrupo")

    def __repr__(self):
        return f'<Subgrupo: {self.id}-{self.nome}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
        self.ativo = form.ativo.data
        self.grupo_id = form.grupo.data

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


class Equipamento(db.Model):
    """    Classe do ativo    """
    # nome do arquivo para cadastro em lote
    nome_doc = 'padrão_equipamentos'
    # titulos para cadastro
    titulos_doc = {'Código*': 'cod', 'Descrição_Curta*': 'descricao_curta', 'Tag*': 'tag',
                   'Subgrupo*': 'subgrupo_id', 'Descrição_Longa': 'descricao_longa', 'Fábrica': 'fabricante',
                   'Marca': 'marca', 'Modelo': 'modelo', 'Número_Série': 'ns', 'Largura': 'largura',
                   'Comprimento': 'comprimento', 'Altura': 'altura', 'Peso': 'peso', 'Potência': 'potencia',
                   'Tensão': 'tensao', 'Ano_Fabricação': 'data_fabricacao', 'Data_Aquisição': 'data_aquisicao',
                   'Data_Instalação': 'data_instalacao', 'Custo_Aquisição': 'custo_aquisicao',
                   'Taxa_Depreciação': 'depreciacao', 'Patrimônio': 'patrimonio', 'Localização': 'localizacao',
                   'Latitude': 'latitude', 'Longitude': 'longitude', 'Centro_Custo': 'centro_custo', 'Ativo': 'ativo'}

    __tablename__ = 'equipamento'
    id = db.Column(db.Integer(), primary_key=True)
    cod = db.Column(db.String(50), nullable=True, index=True)
    descricao_curta = db.Column(db.String(50), nullable=False)
    descricao_longa = db.Column(db.String(50), nullable=True)
    fabricante = db.Column(db.String(50), nullable=True)
    marca = db.Column(db.String(50), nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    ns = db.Column(db.String(50), nullable=True)
    largura = db.Column(db.Integer(), nullable=True)
    comprimento = db.Column(db.Integer(), nullable=True)
    altura = db.Column(db.Integer(), nullable=True)
    peso = db.Column(db.Integer(), nullable=True)
    potencia = db.Column(db.Integer(), nullable=True)
    tensao = db.Column(db.Integer(), nullable=True)

    data_fabricacao = db.Column(db.DateTime(), nullable=True)
    data_aquisicao = db.Column(db.DateTime(), nullable=True)
    data_instalacao = db.Column(db.DateTime(), nullable=True)
    custo_aquisicao = db.Column(db.Float(), nullable=True)
    depreciacao = db.Column(db.Integer(), nullable=True)
    tag = db.Column(db.String(20), nullable=False)
    patrimonio = db.Column(db.String(20), nullable=True)
    localizacao = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    centro_custo = db.Column(db.String(50), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    subgrupo_id = db.Column(db.Integer(), db.ForeignKey("subgrupo.id"), nullable=True)

    subgrupo = db.relationship("Subgrupo", back_populates="equipamento")
    planomanutencao = db.relationship("PlanoManutencao", back_populates="equipamento")
    ordemservico = db.relationship("OrdemServico", back_populates="equipamento")

    def __repr__(self):
        return f'<Equipamento: {self.id}-{self.descricao_curta}>'

    def retornar_ativo(self):
        return self.ativo

    def alterar_ativo(self, ativo):
        self.ativo = ativo

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.cod = form.cod.data
        self.descricao_curta = form.descricao_curta.data.upper()
        self.descricao_longa = form.descricao_longa.data.upper()
        self.fabricante = form.fabricante.data.upper()
        self.marca = form.marca.data.upper()
        self.modelo = form.modelo.data.upper()
        self.ns = form.ns.data.upper()
        self.largura = form.largura.data
        self.comprimento = form.comprimento.data
        self.altura = form.altura.data
        self.peso = form.peso.data
        self.potencia = form.potencia.data
        self.tensao = form.tensao.data
        self.data_fabricacao = form.data_fabricacao.data
        self.data_aquisicao = form.data_aquisicao.data
        self.data_instalacao = form.data_instalacao.data
        self.custo_aquisicao = form.custo_aquisicao.data
        self.depreciacao = form.depreciacao.data
        self.tag = form.tag.data.upper()
        self.patrimonio = form.patrimonio.data
        self.localizacao = form.localizacao.data.upper()
        self.latitude = form.latitude.data
        self.longitude = form.longitude.data
        self.centro_custo = form.centro_custo.data.upper()
        self.ativo = form.ativo.data
        self.subgrupo_id = form.subgrupo.data

    def ativar_desativar(self):
        if self.ativo:
            self.alterar_ativo(False)
        else:
            self.alterar_ativo(True)

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
