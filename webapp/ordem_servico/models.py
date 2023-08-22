import datetime
from dateutil.relativedelta import relativedelta
import logging
from webapp import db
from webapp.plano_manutencao.models import Atividade, ListaAtividade
from sqlalchemy import func
from flask_login import current_user
from flask import flash

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class TipoOrdem(db.Model):
    __tablename__ = 'tipo_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False, index=True)
    plano = db.Column(db.Boolean, nullable=False)
    ordemservico = db.relationship("OrdemServico", back_populates="tipoordem")
    planomanutencao = db.relationship("PlanoManutencao", back_populates="tipoordem")

    def __repr__(self) -> str:
        return f'<Tipo de Ordem: {self.id}-{self.nome}>'


class TipoSituacaoOrdem(db.Model):
    __tablename__ = 'tipo_situacao_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False, index=True)
    ordemservico = db.relationship("OrdemServico", back_populates="tiposituacaoordem")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="tiposituacaoordem")

    def __repr__(self) -> str:
        return f'<Situação de Ordem: {self.id}-{self.nome}>'

    @staticmethod
    def retornar_id_situacao(nome):
        return TipoSituacaoOrdem.query.filter_by(nome=nome).one_or_none().id


class FluxoOrdem(db.Model):
    __tablename__ = 'fluxo_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    de = db.Column(db.Integer(), nullable=False)
    para = db.Column(db.Integer(), nullable=False)

    def __init__(self, de, para):
        self.de = de
        self.para = para

    def __repr__(self) -> str:
        return f'<Fluxo de Ordem: {self.id}-de:{self.de}-para:{self.para}>'


class TramitacaoOrdem(db.Model):
    __tablename__ = 'tramitacao_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    ordemservico_id = db.Column(db.Integer(), db.ForeignKey("ordem_servico.id"), nullable=False)
    usuario_id = db.Column(db.Integer(), db.ForeignKey("usuario.id"), nullable=True)
    tiposituacaoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_situacao_ordem.id"), nullable=False)

    data = db.Column(db.DateTime(), nullable=False)
    observacao = db.Column(db.String(200), nullable=False)

    tiposituacaoordem = db.relationship("TipoSituacaoOrdem", back_populates="tramitacaoordem")
    ordemservico = db.relationship("OrdemServico", back_populates="tramitacaoordem")
    usuario = db.relationship("Usuario", back_populates="tramitacaoordem")

    def __repr__(self) -> str:
        return f'<Tramitação da Ordem: {self.id}-{self.tiposituacaoordem.sigla}-{self.usuario.nome}>'

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

    def alterar_atributos(self, ordem_id, tipo_situacao_id):
        self.ordemservico_id = ordem_id
        self.tiposituacaoordem_id = tipo_situacao_id
        self.usuario_id = current_user.id
        self.observacao = "teste..."
        self.data = datetime.datetime.now()

        # Criando o objeto OrdemServiço
        ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
        # Alterando para a situação da tramitação
        ordem.tiposituacaoordem_id = tipo_situacao_id
        # Cria um objeto SituacaoOrdem
        sit = TipoSituacaoOrdem.query.filter_by(nome="Fiscalizada").one_or_none()
        # Verifica se o id da SituacaoOrdem eh igual ao da tramitacao vigente
        if tipo_situacao_id == sit.id:
            # Caso seja, colocará a data de fechamento da OrdemServico
            ordem.data_fechamento = datetime.datetime.now()
        if ordem.salvar():
            flash("Ordem de Serviço Atualizada", category="success")
        else:
            flash("Ordem de Serviço não Atualizada", category="success")

    @staticmethod
    def insere_tramitacao(descricao, situacao, texto):
        tramitacao = TramitacaoOrdem()
        ordem = OrdemServico.query.filter_by(descricao=descricao).order_by(OrdemServico.id.desc()).first()
        tramitacao.ordemservico_id = ordem.id
        tramitacao.usuario_id = current_user.id
        tramitacao.tiposituacaoordem_id = situacao.id
        tramitacao.observacao = texto
        tramitacao.data = datetime.datetime.now()
        tramitacao.salvar()


class OrdemServico(db.Model):
    __tablename__ = 'ordem_servico'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer())
    descricao = db.Column(db.String(100), nullable=False, index=True)
    data_abertura = db.Column(db.DateTime(), nullable=False)
    data_prevista = db.Column(db.DateTime(), nullable=True)
    data_fechamento = db.Column(db.DateTime(), nullable=True)

    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    tiposituacaoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_situacao_ordem.id"), nullable=False)
    solicitante_id = db.Column(db.Integer(), db.ForeignKey("usuario.id"), nullable=True)
    tipoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_ordem.id"), nullable=False)
    planomanutencao_id = db.Column(db.Integer(), nullable=True)
    listaatividade_id = db.Column(db.Integer(), db.ForeignKey("lista_atividade.id"), nullable=True)

    equipamento = db.relationship("Equipamento", back_populates="ordemservico")
    tiposituacaoordem = db.relationship("TipoSituacaoOrdem", back_populates="ordemservico")
    usuario = db.relationship("Usuario", back_populates="ordemservico")
    tipoordem = db.relationship("TipoOrdem", back_populates="ordemservico")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="ordemservico")
    listaatividade = db.relationship("ListaAtividade", back_populates="ordemservico")

    def __repr__(self) -> str:
        return f'<Ordem de Serviço: {self.id}-{self.descricao}>'

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

    def alterar_atributos(self, form, new, dta_prevista=datetime.datetime.now()):
        """     Função para atribuir valores para ordem a partir de um formulário       """
        if new:
            self.codigo = OrdemServico.gerar_codigo_ordem()
            self.data_abertura = datetime.datetime.now()
            self.data_prevista = dta_prevista
            self.solicitante_id = current_user.id
            self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("Pendente")
            self.tipoordem_id = form.tipo.data
            self.descricao = form.descricao.data.upper()
            self.equipamento_id = form.equipamento.data

    def alterar_atributos_by_plano(self, plano):
        """     Função para atribuir valores para ordem a partir de um plano de manutenção  """
        self.codigo = OrdemServico.gerar_codigo_ordem()
        self.data_abertura = datetime.datetime.now()
        self.solicitante_id = None
        self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("Pendente")
        self.tipoordem_id = plano.tipoordem_id
        self.descricao = plano.nome
        self.equipamento_id = plano.equipamento_id
        self.planomanutencao_id = plano.id
        self.data_prevista = plano.data_inicio
        self.listaatividade_id = plano.listaatividade_id
        ListaAtividade.copiar_lista(plano.listaatividade_id)

        # self.data_prevista = self.data_futura(new, data=plano.data_inicio, tempo=plano.periodicidade.tempo,
        # #                                       unidade=plano.periodicidade.unidade.nome)

    def alterar_atributos_by_ordem(self, ordem, plano):
        self.codigo = OrdemServico.gerar_codigo_ordem()
        self.data_abertura = datetime.datetime.now()
        self.solicitante_id = None
        self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("Pendente")
        self.tipoordem_id = ordem.tipoordem_id
        self.descricao = ordem.descricao
        self.equipamento_id = ordem.equipamento_id
        self.planomanutencao_id = ordem.planomanutencao_id
        self.data_prevista = plano.data_inicio
        self.listaatividade_id = ListaAtividade.copiar_lista(plano.listaatividade_id)

        # self.data_prevista = self.data_futura(new, data=datetime.datetime.now() - datetime.timedelta(days=1),
        #                                       tempo=tempo, unidade=unidade)

    @staticmethod
    def gerar_codigo_ordem():
        """Função para retornar o número para a proxima OS"""
        return db.session.query(func.max(OrdemServico.codigo)).first()[0] + 1

    # def data_futura(self, new, data, tempo, unidade):
    #     """ Função que calcula e retorna uma data no futuro"""
    #     if new:
    #         return data
    #     else:
    #         # Verifica se a base do tempo é dia
    #         if unidade in ["dia", "semana"]:
    #             return data.replace(hour=0, minute=0, second=0, microsecond=0) + \
    #                    datetime.timedelta(days=tempo)
    #         # Verifica se a base do tempo é mensal
    #         if unidade in ["mês", "ano"]:
    #             return data.replace(hour=0, minute=0, second=0, microsecond=0) + \
    #                    relativedelta(months=tempo)
