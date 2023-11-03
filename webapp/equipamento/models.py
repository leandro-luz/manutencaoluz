import logging
from webapp import db
from webapp.utils.objetos import atributo_existe, atribuir_none_id
from flask_login import current_user
from sqlalchemy import func
from unidecode import unidecode

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def verificar_existencia_localizacao_by_nome(model, valor):
    return model.query.filter(model.nome == valor,
                              model.empresa_id == current_user.empresa_id
                              ).one_or_none()


def verificar_existencia_localizacao_by_sigla(model, valor):
    return model.query.filter(model.sigla == valor,
                              model.empresa_id == current_user.empresa_id
                              ).one_or_none()


class Grupo(db.Model):
    """    Classe de grupo de ativos    """

    # titulos para cadastro
    titulos_doc = {'Tipo*': 'tipo', 'Grupo_nome*': 'nome'}

    titulos_csv = {'Grupo_nome'}

    __tablename__ = 'grupo'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="grupo")
    subgrupo = db.relationship("Subgrupo", back_populates="grupo", cascade="all, delete-orphan")

    def __repr__(self):
        return f'{self.nome}'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Subgrupo(db.Model):
    """    Classe de sistemas nos ativos   """

    # titulos para cadastro
    titulos_doc = {'Tipo*': 'tipo', 'Grupo_nome*': 'grupo', 'Subgrupo_nome*': 'nome'}
    titulos_geral_doc = {'Tipo*': 'tipo', 'Grupo_nome*': 'grupo', 'Subgrupo_nome*': 'nome'}

    titulos_csv = {'Grupo_nome; Subgrupo_nome'}

    __tablename__ = 'subgrupo'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    grupo_id = db.Column(db.Integer(), db.ForeignKey("grupo.id"), nullable=True)

    grupo = db.relationship("Grupo", back_populates="subgrupo")
    equipamento = db.relationship("Equipamento", back_populates="subgrupo")

    def __repr__(self):
        return f'{self.grupo.nome}; {self.nome}'

    def alterar_atributos(self, form, grupo_id):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
        self.grupo_id = grupo_id

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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Equipamento(db.Model):
    """    Classe do ativo    """

    # titulos para cadastro
    titulos_doc = {'Codigo*': 'cod', 'Descricao_Curta*': 'descricao_curta', 'Tag*': 'tag',
                   'Subgrupo*': 'subgrupo_id', 'Descricao_Longa': 'descricao_longa', 'Fabrica': 'fabricante',
                   'Marca': 'marca', 'Modelo': 'modelo', 'Numero_Serie': 'ns', 'Largura': 'largura',
                   'Comprimento': 'comprimento', 'Altura': 'altura', 'Peso': 'peso', 'Potencia': 'potencia',
                   'Tensao': 'tensao', 'Ano_Fabricacao': 'data_fabricacao', 'Data_Aquisicao': 'data_aquisicao',
                   'Data_Instalacao': 'data_instalacao', 'Custo_Aquisicao': 'custo_aquisicao',
                   'Taxa_Depreciacao': 'depreciacao', 'Patrimonio': 'patrimonio', 'Localizacao': 'localizacao',
                   'Latitude': 'latitude', 'Longitude': 'longitude', 'Centro_Custo': 'centro_custo', 'Ativo': 'ativo',
                   'Setor': 'setor_id', 'Local': 'local_id', 'Pavimento': 'pavimento_id',
                   'Largura_valor': 'largura_valor', 'Largura_und': 'und_largura_id',
                   'Comprimento_valor': 'comprimento_valor', 'Comprimento_und': 'und_comprimento_id',
                   'Altura_valor': 'altura_valor', 'Altura_und': 'und_altura_id',
                   'Peso_valor': 'peso_valor', 'Peso_und': 'und_peso_id',
                   'Vazao_valor': 'vazao_valor', 'Vazao_und': 'und_vazao_id',
                   'Volume_valor': 'volume_valor', 'Volume_und': 'und_volume_id',
                   'Area_valor': 'area_valor', 'Area_und': 'und_area_id',
                   'Potencia_valor': 'potencia_valor', 'Potencia_und': 'und_potencia_id',
                   'Tensao_valor': 'tensao_valor', 'Tensao_und': 'und_tensao_id'
                   }

    titulos_csv = {'cod; descricao_curta; descricao_longa; fabricante; marca; modelo; ns; data_fabricacao; '
                   'data_aquisicao; data_instalacao; custo_aquisicao; depreciacao; tag; patrimonio; '
                   'latitude; longitude; centro_custo; ativo; subgrupo_nome; setor_nome; local_nome; pavimento_nome; '
                   'largura_valor; comprimento_valor; altura_valor; peso_valor; vazao_valor; volume_valor; area_valor; '
                   'potencia_valor; tensao_valor; und_comprimento_unidade; und_largura_unidade; und_altura_unidade; '
                   'und_peso_nome; und_vazao_nome; und_volume_nome; und_area_nome; und_potencia_nome; und_tensao_nome'}

    __tablename__ = 'equipamento'
    id = db.Column(db.Integer(), primary_key=True)
    cod = db.Column(db.String(50), nullable=True, index=True)
    descricao_curta = db.Column(db.String(50), nullable=False)
    descricao_longa = db.Column(db.String(50), nullable=True)
    fabricante = db.Column(db.String(50), nullable=True)
    marca = db.Column(db.String(50), nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    ns = db.Column(db.String(50), nullable=True)

    data_fabricacao = db.Column(db.DateTime(), nullable=True)
    data_aquisicao = db.Column(db.DateTime(), nullable=True)
    data_instalacao = db.Column(db.DateTime(), nullable=True)
    custo_aquisicao = db.Column(db.Float(), nullable=True)
    depreciacao = db.Column(db.Integer(), nullable=True)
    tag = db.Column(db.String(30), nullable=True)
    patrimonio = db.Column(db.String(20), nullable=True)

    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    centro_custo = db.Column(db.String(50), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)
    subgrupo_id = db.Column(db.Integer(), db.ForeignKey("subgrupo.id"), nullable=False)
    setor_id = db.Column(db.Integer(), db.ForeignKey("setor.id"), nullable=True)
    local_id = db.Column(db.Integer(), db.ForeignKey("local.id"), nullable=True)
    pavimento_id = db.Column(db.Integer(), db.ForeignKey("pavimento.id"), nullable=True)

    largura_valor = db.Column(db.Float(), nullable=True)
    comprimento_valor = db.Column(db.Float(), nullable=True)
    altura_valor = db.Column(db.Float(), nullable=True)
    peso_valor = db.Column(db.Float(), nullable=True)
    vazao_valor = db.Column(db.Float(), nullable=True)
    volume_valor = db.Column(db.Float(), nullable=True)
    area_valor = db.Column(db.Float(), nullable=True)
    potencia_valor = db.Column(db.Float(), nullable=True)
    tensao_valor = db.Column(db.Float(), nullable=True)

    und_comprimento_id = db.Column(db.Integer(), db.ForeignKey("tipo_comprimento.id"), nullable=True)
    und_largura_id = db.Column(db.Integer(), db.ForeignKey("tipo_comprimento.id"), nullable=True)
    und_altura_id = db.Column(db.Integer(), db.ForeignKey("tipo_comprimento.id"), nullable=True)
    und_peso_id = db.Column(db.Integer(), db.ForeignKey("tipo_peso.id"), nullable=True)
    und_vazao_id = db.Column(db.Integer(), db.ForeignKey("tipo_vazao.id"), nullable=True)
    und_volume_id = db.Column(db.Integer(), db.ForeignKey("tipo_volume.id"), nullable=True)
    und_area_id = db.Column(db.Integer(), db.ForeignKey("tipo_area.id"), nullable=True)

    und_potencia_id = db.Column(db.Integer(), db.ForeignKey("tipo_potencia.id"), nullable=True)
    und_tensao_id = db.Column(db.Integer(), db.ForeignKey("tipo_tensao_eletrica.id"), nullable=True)

    empresa = db.relationship("Empresa", back_populates="equipamento")
    subgrupo = db.relationship("Subgrupo", back_populates="equipamento")
    planomanutencao = db.relationship("PlanoManutencao", back_populates="equipamento", cascade="all, delete-orphan")
    ordemservico = db.relationship("OrdemServico", back_populates="equipamento", cascade="all, delete-orphan")
    setor = db.relationship("Setor", back_populates="equipamento")
    local = db.relationship("Local", back_populates="equipamento")
    pavimento = db.relationship("Pavimento", back_populates="equipamento")

    comprimento = db.relationship("Comprimento", backref="comprimento_", foreign_keys=[und_comprimento_id])
    largura = db.relationship("Comprimento", backref="largura_", foreign_keys=[und_largura_id])
    altura = db.relationship("Comprimento", backref="altura_", foreign_keys=[und_altura_id])

    peso = db.relationship("Peso", back_populates="equipamento")
    vazao = db.relationship("Vazao", back_populates="equipamento")
    volume = db.relationship("Volume", back_populates="equipamento")
    area = db.relationship("Area", back_populates="equipamento")
    potencia = db.relationship("Potencia", back_populates="equipamento")
    tensaoeletrica = db.relationship("TensaoEletrica", back_populates="equipamento")

    def __repr__(self) -> str:
        return f'{self.cod}; {self.descricao_curta}; {self.descricao_longa}; {self.fabricante}; ' \
               f'{self.marca}; {self.modelo}; {self.ns}; {self.data_fabricacao}; {self.data_aquisicao}; ' \
               f'{self.data_instalacao}; {self.custo_aquisicao}; {self.depreciacao}; {self.tag}; {self.patrimonio}; ' \
               f'{self.latitude}; {self.longitude}; {self.centro_custo}; {self.ativo}; ' \
               f'{atributo_existe(self, "subgrupo", "nome")};' \
               f'{atributo_existe(self, "setor", "nome")}; {atributo_existe(self, "local", "nome")}; ' \
               f'{atributo_existe(self, "pavimento", "nome")}; {self.largura_valor}; {self.comprimento_valor}; ' \
               f'{self.altura_valor}; {self.peso_valor}; {self.vazao_valor}; {self.volume_valor}; {self.area_valor}; ' \
               f'{self.potencia_valor}; {self.tensao_valor}; {atributo_existe(self, "comprimento", "unidade")}; ' \
               f'{atributo_existe(self, "largura", "unidade")}; {atributo_existe(self, "altura", "unidade")}; ' \
               f'{atributo_existe(self, "peso", "unidade")}; {atributo_existe(self, "vazao", "unidade")}; ' \
               f'{atributo_existe(self, "volume", "unidade")}; {atributo_existe(self, "area", "unidade")}; ' \
               f'{atributo_existe(self, "potencia", "unidade")}; {atributo_existe(self, "tensaoeletrica", "unidade")}'

    def retornar_ativo(self):
        return self.ativo

    def alterar_ativo(self, ativo):
        self.ativo = ativo

    def alterar_atributos(self, form, new):
        """    Função para alterar os atributos do objeto    """
        self.cod = self.gerar_codigo(form, new)
        self.tag = self.gerar_tag(form, new)
        self.empresa_id = current_user.empresa_id
        self.descricao_curta = form.descricao_curta.data.upper()
        self.descricao_longa = form.descricao_longa.data.upper()
        self.fabricante = form.fabricante.data.upper()
        self.marca = form.marca.data.upper()
        self.modelo = form.modelo.data.upper()
        self.ns = form.ns.data.upper()
        self.data_fabricacao = form.data_fabricacao.data
        self.data_aquisicao = form.data_aquisicao.data
        self.data_instalacao = form.data_instalacao.data
        self.custo_aquisicao = form.custo_aquisicao.data
        self.depreciacao = form.depreciacao.data
        self.patrimonio = form.patrimonio.data.upper()
        self.latitude = form.latitude.data
        self.longitude = form.longitude.data
        self.centro_custo = form.centro_custo.data.upper()
        self.ativo = form.ativo.data
        self.subgrupo_id = form.subgrupo.data
        self.setor_id = atribuir_none_id(form.setor.data)
        self.local_id = atribuir_none_id(form.local.data)
        self.pavimento_id = atribuir_none_id(form.pavimento.data)
        self.largura_valor = form.largura_valor.data
        self.und_largura_id = atribuir_none_id(form.und_largura.data)
        self.comprimento_valor = form.comprimento_valor.data
        self.und_comprimento_id = atribuir_none_id(form.und_comprimento.data)
        self.altura_valor = form.altura_valor.data
        self.und_altura_id = atribuir_none_id(form.und_altura.data)
        self.peso_valor = form.peso_valor.data
        self.und_peso_id = atribuir_none_id(form.und_peso.data)
        self.vazao_valor = form.vazao_valor.data
        self.und_vazao_id = atribuir_none_id(form.und_vazao.data)
        self.volume_valor = form.volume_valor.data
        self.und_volume_id = atribuir_none_id(form.und_volume.data)
        self.area_valor = form.area_valor.data
        self.und_area_id = atribuir_none_id(form.und_area.data)
        self.peso_valor = form.peso_valor.data
        self.und_peso_id = atribuir_none_id(form.und_peso.data)
        self.potencia_valor = form.potencia_valor.data
        self.und_potencia_id = atribuir_none_id(form.und_potencia.data)
        self.tensao_valor = form.tensao_valor.data
        self.und_tensao_id = atribuir_none_id(form.und_tensao.data)

    def ativar_desativar(self):
        """Função para ativar e desativar """
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

    def gerar_codigo(self, form, new):
        """Função que gera automático o código do equipamento"""
        if new:
            posicao = db.session.query(func.max(Equipamento.id)).first()[0]
            if posicao:
                posicao += 1
            else:
                posicao = 1
        else:
            posicao = self.id

        if form.cod_automatico.data or not form.cod:
            subgrupo = Subgrupo.query.filter_by(id=form.subgrupo.data).one_or_none()
            return (str(subgrupo.grupo.empresa_id).zfill(5) + "." +
                    unidecode(str(subgrupo.grupo.nome)[:3]) +
                    str(subgrupo.grupo.id).zfill(5) + "." +
                    unidecode(str(subgrupo.nome)[:3]) +
                    str(subgrupo.id).zfill(5) + "." +
                    unidecode(str(self.descricao_curta)[:3]) +
                    str(posicao).zfill(5))
        else:
            return form.cod.data

    def gerar_tag(self, form, new):
        """Função que gera automático o tag do equipamento"""
        if new:
            posicao = db.session.query(func.max(Equipamento.id)).first()[0]
            if posicao:
                posicao += 1
            else:
                posicao = 1
        else:
            posicao = self.id

        if form.tag_automatico.data or not form.tag:
            set = Setor.query.filter_by(id=form.setor.data).one_or_none()
            loc = Local.query.filter_by(id=form.local.data).one_or_none()
            pav = Pavimento.query.filter_by(id=form.pavimento.data).one_or_none()
            return (unidecode(str(set.sigla)) + "." +
                    unidecode(str(loc.sigla)) + "." +
                    unidecode(str(pav.sigla)) + "." +
                    unidecode(str(self.descricao_curta)[:3]) +
                    str(posicao).zfill(5))
        else:
            return form.tag.data


class Pavimento(db.Model):
    """    Classe de grupo de ativos    """

    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Sigla*': 'sigla'}

    titulos_csv = {'Nome; Sigla'}

    __tablename__ = 'pavimento'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False)

    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="pavimento")
    equipamento = db.relationship("Equipamento", back_populates="pavimento")

    def __repr__(self):
        return f'{self.nome}; {self.sigla}'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        if form.nome.data:
            self.nome = form.nome.data.upper()
        if form.sigla.data:
            self.sigla = form.sigla.data.upper()
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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Setor(db.Model):
    """    Classe de grupo de ativos    """

    # titulos para cadastro
    titulos_doc = {'Tipo*': 'tipo', 'Nome*': 'nome', 'Sigla*': 'sigla'}

    titulos_csv = {'Nome; Sigla'}

    __tablename__ = 'setor'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="setor")
    equipamento = db.relationship("Equipamento", back_populates="setor")

    def __repr__(self):
        return f'{self.nome}; {self.sigla}'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        if form.nome.data:
            self.nome = form.nome.data.upper()
        if form.sigla.data:
            self.sigla = form.sigla.data.upper()
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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Local(db.Model):
    """    Classe de grupo de ativos    """

    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Sigla*': 'sigla'}

    titulos_csv = {'Nome; Sigla'}

    __tablename__ = 'local'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False)
    empresa_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="local")
    equipamento = db.relationship("Equipamento", back_populates="local")

    def __repr__(self):
        return f'{self.nome}; {self.sigla}'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        if form.nome.data:
            self.nome = form.nome.data.upper()
        if form.sigla.data:
            self.sigla = form.sigla.data.upper()
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

    def excluir(self) -> bool:
        """    Função para retirar do banco de dados o objeto"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro Deletar objeto no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Volume(db.Model):
    """    Classe de Volume    """

    __tablename__ = 'tipo_volume'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="volume")

    def __repr__(self):
        return f'<Volume: {self.id}-{self.unidade}>'


class Vazao(db.Model):
    """    Classe de Vazao    """

    __tablename__ = 'tipo_vazao'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="vazao")

    def __repr__(self):
        return f'<Vazao: {self.id}-{self.unidade}>'


class Area(db.Model):
    """    Classe de Area    """

    __tablename__ = 'tipo_area'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="area")

    def __repr__(self):
        return f'<Area: {self.id}-{self.unidade}>'


class Peso(db.Model):
    """    Classe de Peso    """

    __tablename__ = 'tipo_peso'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="peso")

    def __repr__(self):
        return f'<Peso: {self.id}-{self.unidade}>'


class Comprimento(db.Model):
    """    Classe de Distancia    """

    __tablename__ = 'tipo_comprimento'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Comprimento: {self.id}-{self.unidade}>'


class Potencia(db.Model):
    """    Classe de Distancia    """

    __tablename__ = 'tipo_potencia'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="potencia")

    def __repr__(self):
        return f'<Potencia: {self.id}-{self.unidade}>'


class TensaoEletrica(db.Model):
    """    Classe de Distancia    """

    __tablename__ = 'tipo_tensao_eletrica'
    id = db.Column(db.Integer(), primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    equipamento = db.relationship("Equipamento", back_populates="tensaoeletrica")

    def __repr__(self):
        return f'<Tensão Elétrica: {self.id}-{self.unidade}>'
