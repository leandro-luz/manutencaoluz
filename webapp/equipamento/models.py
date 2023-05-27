import logging
from webapp import db
from flask_login import current_user

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class Sistema(db.Model):
    """    Classe de sistemas nos ativos   """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="sistema")

    def __repr__(self):
        return f'<Sistema: {self.id}-{self.nome}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data
        self.ativo = form.ativo.data


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


class Grupo(db.Model):
    """    Classe de grupo de ativos    """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    empresa_id = db.Column(db.Integer(), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="grupo")

    def __repr__(self):
        return f'<Grupo: {self.id}-{self.nome}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data
        self.ativo = form.ativo.data
        self.empresa_id = current_user.empresa_id

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


class Equipamento(db.Model):
    """    Classe do ativo    """
    # nome do arquivo para cadastro em lote
    nome_doc = 'padrão_equipamentos'
    # titulos para cadastro
    titulos_doc = ['Código*', 'Descrição_Curta*', 'Tag*', 'Descrição_Longa', 'Fábrica', 'Marca', 'Modelo',
              'Número_Série', 'Largura', 'Comprimento', 'Altura', 'Peso','Potência', 'Tensão', 'Ano_Fabricação',
              'Data_Aquisição', 'Data_Instalação', 'Custo_Aquisição', 'Taxa_Depreciação',
              'Patrimônio', 'Localização', 'Centro_Custo', 'Grupo_Equipamentos', 'Sistema', 'Ativo']
   # titulos obrigatórios
    titulos_obg = ['Código*', 'Descrição_Curta*','Tag*']

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
    custo_aquisicao = db.Column(db.Integer(), nullable=True)
    depreciacao = db.Column(db.Integer(), nullable=True)
    tag = db.Column(db.String(20), nullable=False)
    patrimonio = db.Column(db.String(20), nullable=True)
    localizacao = db.Column(db.String(50), nullable=True)
    centro_custo = db.Column(db.String(50), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    grupo_id = db.Column(db.Integer(), db.ForeignKey("grupo.id"), nullable=False, default=0)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    grupo = db.relationship("Grupo", back_populates="equipamento")
    empresa = db.relationship("Empresa", back_populates="equipamento")
    sistema = db.relationship("Sistema", back_populates="equipamento")
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
        self.descricao_curta = form.descricao_curta.data
        self.descricao_longa = form.descricao_longa.data
        self.fabricante = form.fabricante.data
        self.marca = form.marca.data
        self.modelo = form.modelo.data
        self.ns = form.ns.data
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
        self.tag = form.tag.data
        self.patrimonio = form.patrimonio.data
        self.localizacao = form.localizacao.data
        self.centro_custo = form.centro_custo.data
        self.ativo = form.ativo.data
        self.grupo_id = form.grupo.data
        self.empresa_id = current_user.empresa_id

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
