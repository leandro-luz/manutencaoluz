import logging
import datetime
from dateutil.relativedelta import relativedelta
from webapp import db
from flask import flash

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

    def __init__(self, nome, tempo, unidade_id) -> None:
        self.nome = nome
        self.tempo = tempo
        self.unidade_id = unidade_id

    def __repr__(self):
        return f'<Periodicidade: {self.id}-{self.nome}>'


class PlanoManutencao(db.Model):
    """    Classe de Plano de Manutenção   """
    nome_doc = 'padrão_plano_manutenção'
    # titulos para cadastro
    titulos_doc = {'Nome*': 'nome', 'Código*': 'codigo', 'Tipo_Ordem*': 'tipoordem_id',
                   'Tipo_Data_Inicial*': 'tipodata_id', 'Data_Início*': 'data_inicio',
                   'Periodicidade*': 'periodicidade_id', 'Equipamento_cod*': 'equipamento_id'}

    __tablename__ = 'plano_manutencao'

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    codigo = db.Column(db.String(50), nullable=False, index=True)
    data_inicio = db.Column(db.DateTime(), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    tipodata_id = db.Column(db.Integer(), db.ForeignKey("tipo_data.id"), nullable=False)
    periodicidade_id = db.Column(db.Integer(), db.ForeignKey("periodicidade.id"), nullable=False)
    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    tipoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_ordem.id"), nullable=False)

    tipodata = db.relationship("TipoData", back_populates="planomanutencao")
    periodicidade = db.relationship("Periodicidade", back_populates="planomanutencao")
    equipamento = db.relationship("Equipamento", back_populates="planomanutencao")
    tipoordem = db.relationship("TipoOrdem", back_populates="planomanutencao")

    def __repr__(self):
        return f'<Plano de Manutenção: {self.id}-{self.codigo}>'

    def alterar_atributos(self, form, new):
        """    Função para alterar os atributos do objeto    """
        self.nome = form.nome.data.upper()
        self.codigo = form.codigo.data
        self.ativo = form.ativo.data
        self.tipoordem_id = form.tipoordem.data
        self.tipodata_id = form.tipodata.data
        self.periodicidade_id = form.periodicidade.data
        self.equipamento_id = form.equipamento.data
        self.data_inicio = form.data_inicio.data

        if new:
            try:
                self.alterar_tipo_situacao()
            except:
                flash("Tipo Situação do Plano não encontrado", category="danger")

    def alterar_ativo(self, ativo):
        self.ativo = ativo

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

    def alterar_data_prevista(self, new):
        self.data_inicio = self.data_futura(new,
                                            self.data_inicio,
                                            self.periodicidade.tempo,
                                            self.periodicidade.unidade.nome)

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
