import logging
import datetime
from dateutil.relativedelta import relativedelta
from webapp import db
# from webapp.ordem_servico.models import TipoOrdem
from webapp.equipamento.models import Equipamento
from sqlalchemy import func
from unidecode import unidecode

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class TipoData(db.Model):
    """    Classe de tipos de datas (data fixa/móvel)   """
    __tablename__ = 'tipo_data'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    planomanutencao = db.relationship("PlanoManutencao", back_populates="tipodata")

    def __repr__(self):
        return f'<TipoData: {self.id}-{self.nome}>'


class Unidade(db.Model):
    """    Classe de tipos de periodicidade   """
    __tablename__ = 'unidade'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    periodicidade = db.relationship("Periodicidade", back_populates="unidade")

    def __repr__(self):
        return f'<Periodicidade: {self.id}-{self.nome}>'


class Periodicidade(db.Model):
    """    Classe de tipos de periodicidade   """
    __tablename__ = 'periodicidade'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    tempo = db.Column(db.Integer(), nullable=False)

    unidade_id = db.Column(db.Integer(), db.ForeignKey("unidade.id"), nullable=False)

    unidade = db.relationship("Unidade", back_populates="periodicidade")
    planomanutencao = db.relationship("PlanoManutencao", back_populates="periodicidade")

    def __repr__(self):
        return f'<Periodicidade: {self.id}-{self.nome}>'


class TipoParametro(db.Model):
    """    Classe de atividade da lista de atividades   """
    __tablename__ = 'tipo_parametro'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), nullable=False, index=True)

    atividade = db.relationship("Atividade", back_populates="tipoparametro")

    def __repr__(self):
        return f'<TipoParametro: {self.id}-{self.nome}>'


class ListaAtividade(db.Model):
    """    Classe de lista de atividades  """
    __tablename__ = 'lista_atividade'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(20), nullable=False, index=True)
    data = db.Column(db.DateTime(), nullable=True)
    observacao = db.Column(db.String(500), nullable=True)

    atividade = db.relationship("Atividade", back_populates="listaatividade", cascade="all, delete-orphan")
    planomanutencao = db.relationship("PlanoManutencao", back_populates="listaatividade")
    ordemservico = db.relationship("OrdemServico", back_populates="listaatividade")

    def __repr__(self):
        return f'<ListaAtividade: {self.id}-{self.nome}>'

    def alterar_atributos(self):
        """    Função para alterar os atributos do objeto    """
        self.data = datetime.datetime.now()
        self.nome = self.data.strftime("%Y%m%d%H%M%S")

    def alterar_observacao(self, observacao):
        """Função para alterar o campo observação"""
        self.observacao = observacao
        self.salvar()

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

    def clone(self):
        d = dict(self.__dict__)
        d.pop("id")  # get rid of id
        d.pop("_sa_instance_state")  # get rid of SQLAlchemy special attr
        copy = self.__class__(**d)
        db.session.add(copy)
        db.session.commit()
        return copy

    @staticmethod
    def copiar_lista(listaatividade_id, new=False):
        """Função que copia a lista de atividades e suas atividades vinculadas"""
        valor = 0
        # busca a listaatividade vinculada ao plano
        listaatividade_antiga = ListaAtividade.query.filter_by(id=listaatividade_id).one_or_none()
        # Se a lista antiga existir
        if listaatividade_antiga:
            listaatividade_nova = ListaAtividade()
            if new:
                listaatividade_nova.alterar_atributos()
            else:
                # Criar uma copia do lista antiga
                listaatividade_nova = listaatividade_antiga.clone()
                listaatividade_nova.data = datetime.datetime.now()
            listaatividade_nova.salvar()
            # retorna o id da nova lista
            valor = listaatividade_nova.id
            # Copiar as atividades para a nova lista
            Atividade.clone(listaatividade_id, listaatividade_nova.id)
        return valor


class TipoBinario(db.Model):
    """    Classe de lista de atividades  """
    __tablename__ = 'tipo_binario'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(20), nullable=False, index=True)

    atividade = db.relationship("Atividade", back_populates="tipobinario")

    def __repr__(self):
        return f'<TipoBinário: {self.id}-{self.nome}>'


class Atividade(db.Model):
    """    Classe de atividades  """
    __tablename__ = 'atividade'
    id = db.Column(db.Integer(), primary_key=True)
    posicao = db.Column(db.Integer(), nullable=False)
    descricao = db.Column(db.String(100), nullable=False, index=True)

    valorinteiro = db.Column(db.Integer(), nullable=True)
    valordecimal = db.Column(db.Float(), nullable=True)
    valortexto = db.Column(db.String(100), nullable=True)

    valorbinario_id = db.Column(db.Integer(), db.ForeignKey("tipo_binario.id"), nullable=True)
    tipoparametro_id = db.Column(db.Integer(), db.ForeignKey("tipo_parametro.id"), nullable=False)
    listaatividade_id = db.Column(db.Integer(), db.ForeignKey("lista_atividade.id"), nullable=False)

    listaatividade = db.relationship("ListaAtividade", back_populates="atividade")
    tipoparametro = db.relationship("TipoParametro", back_populates="atividade")
    tipobinario = db.relationship("TipoBinario", back_populates="atividade")

    def __repr__(self):
        return f'<Atividade: {self.id}-{self.posicao}-{self.descricao}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.posicao = form.posicao.data
        self.descricao = form.descricao.data
        self.tipoparametro_id = form.tipoparametro_id.data
        self.listaatividade_id = form.listaatividade_id.data

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

    @staticmethod
    def clone(listaantiga_id, listanova_id):
        """     Função para criar os clones das atividades de uma nova lista de atividades"""

        # Busca as atividades antigas
        atividades_antigas = Atividade.query.filter_by(listaatividade_id=listaantiga_id).all()

        # Gera a lista de atividades novas
        atividades_novas = [
            Atividade(
                posicao=atividade.posicao,
                descricao=atividade.descricao,
                valorbinario_id=atividade.valorbinario_id,
                tipoparametro_id=atividade.tipoparametro_id,
                listaatividade_id=listanova_id)
            for atividade in atividades_antigas]

        try:
            # Adicionando as novas atividades na sessão e realizando o commit
            db.session.add_all(atividades_novas)
            db.session.commit()
        except Exception as e:
            log.error(f'Erro salvar no banco de dados:{e}')
            db.session.rollback()


class PlanoManutencao(db.Model):
    """    Classe de Plano de Manutenção   """

    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Codigo*': 'codigo', 'Tipo_Ordem*': 'tipoordem_id',
                   'Tipo_Data_Inicial*': 'tipodata_id', 'Data_Inicio*': 'data_inicio',
                   'Periodicidade*': 'periodicidade_id', 'Equipamento_cod*': 'equipamento_id'}

    titulos_csv = {'nome; codigo; data_inicio; ativo; total_tecnico; tempo_estimado; revisao;'
                   'tipodata_nome; periodicidade_nome; equipamento_descricao_curta; tipoordem_nome'}

    __tablename__ = 'plano_manutencao'

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    codigo = db.Column(db.String(50), nullable=False, index=True)
    data_inicio = db.Column(db.DateTime(), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    total_tecnico = db.Column(db.Integer(), nullable=False)
    tempo_estimado = db.Column(db.Float(), nullable=False)
    revisao = db.Column(db.Integer(), nullable=False, default=0)

    tipodata_id = db.Column(db.Integer(), db.ForeignKey("tipo_data.id"), nullable=False)
    periodicidade_id = db.Column(db.Integer(), db.ForeignKey("periodicidade.id"), nullable=False)
    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    tipoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_ordem.id"), nullable=False)
    listaatividade_id = db.Column(db.Integer(), db.ForeignKey("lista_atividade.id"), nullable=True)

    tipodata = db.relationship("TipoData", back_populates="planomanutencao")
    periodicidade = db.relationship("Periodicidade", back_populates="planomanutencao")
    equipamento = db.relationship("Equipamento", back_populates="planomanutencao")
    tipoordem = db.relationship("TipoOrdem", back_populates="planomanutencao")
    listaatividade = db.relationship("ListaAtividade", back_populates="planomanutencao")

    def __repr__(self):
        return f'{self.nome}; {self.codigo}; {self.data_inicio}; {self.ativo}; {self.total_tecnico}; ' \
               f'{self.tempo_estimado}; {self.revisao}; {self.tipodata.nome}; {self.periodicidade.nome}; ' \
               f'{self.equipamento.descricao_curta}; {self.tipoordem.nome}'

    def alterar_atributos(self, form, new):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
        self.codigo = self.gerar_codigo(form, new)
        self.tipoordem_id = form.tipoordem.data
        self.tipodata_id = form.tipodata.data
        self.periodicidade_id = form.periodicidade.data
        self.equipamento_id = form.equipamento.data
        self.data_inicio = form.data_inicio.data
        self.total_tecnico = form.total_tecnico.data
        self.tempo_estimado = form.tempo_estimado.data

    def alterar_lista(self, listaatividade_id, alterar_revisao):
        self.listaatividade_id = listaatividade_id
        if alterar_revisao:
            self.revisao += 1
        self.salvar()

    def alterar_ativo(self, ativo):
        self.ativo = ativo

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
            posicao = db.session.query(func.max(PlanoManutencao.id)).first()[0] + 1
        else:
            posicao = self.id

        if form.cod_automatico.data or not form.codigo:
            equipamento = Equipamento.query.filter_by(id=form.equipamento.data).one_or_none()

            return (unidecode(str(equipamento.descricao_curta)[:3]) +
                    str(form.tipoordem.data).zfill(2) + "." +
                    str(form.tipodata.data).zfill(2) +
                    str(form.periodicidade.data).zfill(2) + "." +
                    str(posicao).zfill(4))
        else:
            return form.codigo.data

    @staticmethod
    def salvar_lote(lote):
        """Função para salvar em lote"""
        try:
            db.session.add_all(lote)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar ao tentar salvar o lote:{e}')
            db.session.rollback()
        return False

    def alterar_data_prevista(self, new):
        self.data_inicio = self.data_futura(new,
                                            self.data_inicio,
                                            self.periodicidade.tempo,
                                            self.periodicidade.nome.nome)

    @staticmethod
    def data_futura(new, data, tempo, unidade):
        """ Função que calcula e retorna uma data no futuro"""
        if new:
            return data
        else:
            # Verifica se a base do tempo é hora
            if unidade in ["hora"]:
                return data.replace(minute=0, second=0, microsecond=0) + \
                       datetime.timedelta(hours=tempo)
            # Verifica se a base do tempo é dia
            if unidade in ["dia", "semana"]:
                return data.replace(hour=0, minute=0, second=0, microsecond=0) + \
                       datetime.timedelta(days=tempo)
            # Verifica se a base do tempo é mensal
            if unidade in ["mês", "ano"]:
                return data.replace(hour=0, minute=0, second=0, microsecond=0) + \
                       relativedelta(months=tempo)

    @staticmethod
    def retornar_codigo_plano(plano_id):
        if plano_id:
            plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
            return plano.codigo
        else:
            return None
