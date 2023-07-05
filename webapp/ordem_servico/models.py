import datetime
import logging
from webapp import db
from sqlalchemy import func
from flask_login import current_user

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



class SituacaoOrdem(db.Model):
    __tablename__ = 'situacao_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False, index=True)
    ordemservico = db.relationship("OrdemServico", back_populates="situacaoordem")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="situacaoordem")

    # def __init__(self, nome, sigla, descricao):
    #     self.nome = nome
    #     self.sigla = sigla
    #     self.descricao = descricao

    def __repr__(self) -> str:
        return f'<Situação de Ordem: {self.id}-{self.nome}>'


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
    situacaoordem_id = db.Column(db.Integer(), db.ForeignKey("situacao_ordem.id"), nullable=False)

    data = db.Column(db.DateTime(), nullable=False)
    observacao = db.Column(db.String(200), nullable=False)

    situacaoordem = db.relationship("SituacaoOrdem", back_populates="tramitacaoordem")
    ordemservico = db.relationship("OrdemServico", back_populates="tramitacaoordem")
    usuario = db.relationship("Usuario", back_populates="tramitacaoordem")

    def __repr__(self) -> str:
        return f'<Tramitação da Ordem: {self.id}-{self.situacaoordem.sigla}-{self.usuario.nome}>'

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

    def alterar_atributos(self, form, ordem_id):
        self.ordemservico_id = ordem_id
        self.usuario_id = current_user.id
        self.situacaoordem_id = form.situacaoordem.data
        self.observacao = form.observacao.data.upper()
        self.data = datetime.datetime.now()

        # Criando o objeto OrdemServiço
        ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
        # Alterando para a situação da tramitação
        ordem.situacaoordem_id = form.situacaoordem.data
        # Cria um objeto SituacaoOrdem
        sit = SituacaoOrdem.query.filter_by(nome="Fiscalizada").one_or_none()
        # Verifica se o id da SituacaoOrdem eh igual ao da tramitacao vigente
        if form.situacaoordem.data == sit.id:
            # Caso seja, colocará a data de fechamento da OrdemServico
            ordem.data_fechamento = datetime.datetime.now()
        ordem.salvar()

    @staticmethod
    def insere_tramitacao(descricao, situacao, texto):
        tramitacao = TramitacaoOrdem()
        ordem = OrdemServico.query.filter_by(descricao=descricao).order_by(OrdemServico.id.desc()).first()
        tramitacao.ordemservico_id = ordem.id
        tramitacao.usuario_id = current_user.id
        tramitacao.situacaoordem_id = situacao.id
        tramitacao.observacao = texto
        tramitacao.data = datetime.datetime.now()
        tramitacao.salvar()


class OrdemServico(db.Model):
    __tablename__ = 'ordem_servico'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer())
    descricao = db.Column(db.String(100), nullable=False, index=True)
    data_abertura = db.Column(db.DateTime(), nullable=False)
    data_fechamento = db.Column(db.DateTime(), nullable=True)

    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    situacaoordem_id = db.Column(db.Integer(), db.ForeignKey("situacao_ordem.id"), nullable=False)
    solicitante_id = db.Column(db.Integer(), db.ForeignKey("usuario.id"), nullable=False)
    tipoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_ordem.id"), nullable=False)
    planomanutencao_id = db.Column(db.Integer(), nullable=True)

    equipamento = db.relationship("Equipamento", back_populates="ordemservico")
    situacaoordem = db.relationship("SituacaoOrdem", back_populates="ordemservico")
    usuario = db.relationship("Usuario", back_populates="ordemservico")
    tipoordem = db.relationship("TipoOrdem", back_populates="ordemservico")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="ordemservico")

    def __repr__(self) -> str:
        return f'<Ordem de Serviço: {self.id}-{self.descricao}-' \
               f'{self.equipamento.descricao_curta}-{self.situacaoordem.nome}>'

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

    def alterar_atributos(self, form, new):
        if new:
            consulta = db.session.query(func.max(OrdemServico.codigo))
            self.codigo = consulta.first()[0]+1
            self.data_abertura = datetime.datetime.now()
            self.solicitante_id = current_user.id
            # Inserindo o id da situação "Pendente" na OrdemServico
            sit = SituacaoOrdem.query.filter_by(nome="Pendente").one_or_none()
            self.situacaoordem_id = sit.id
            self.tipoordem_id = form.tipo.data
            self.descricao = form.descricao.data.upper()
            self.equipamento_id = form.equipamento.data
