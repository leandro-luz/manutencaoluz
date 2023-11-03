import datetime
import logging
from webapp import db
from webapp.plano_manutencao.models import ListaAtividade, PlanoManutencao
from webapp.usuario.models import PerfilManutentorUsuario
from webapp.utils.objetos import atributo_existe
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
    texto_atual = db.Column(db.String(20), nullable=False)
    texto_futuro = db.Column(db.String(20), nullable=False)

    ordemservico = db.relationship("OrdemServico", back_populates="tiposituacaoordem")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="tiposituacaoordem")

    tiposituacaoordemperfilmanutentor = db.relationship("TipoSituacaoOrdemPerfilManutentor",
                                                        back_populates="tiposituacaoordem")

    def __repr__(self) -> str:
        return f'<Situação de Ordem: {self.id}-{self.nome}>'

    @staticmethod
    def retornar_id_situacao(sigla):
        return TipoSituacaoOrdem.query.filter_by(sigla=sigla).one_or_none().id


class TipoStatusOrdem(db.Model):
    __tablename__ = 'tipo_status_ordem'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    sigla = db.Column(db.String(5), nullable=False, index=True)

    ordemservico = db.relationship("OrdemServico", back_populates="tipostatusordem")

    def __repr__(self) -> str:
        return f'<Status de Ordem: {self.id}-{self.nome}>'

    @staticmethod
    def retornar_id_status(sigla):
        return TipoStatusOrdem.query.filter_by(sigla=sigla).one_or_none().id


class TipoSituacaoOrdemPerfilManutentor(db.Model):
    """    Classe relacionamento entre Tela e PerfilAcesso    """
    __tablename__ = 'tipo_situacao_ordem_perfil_manutentor'
    id = db.Column(db.Integer(), primary_key=True)

    tiposituacaoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_situacao_ordem.id"), nullable=False)
    perfilmanutentor_id = db.Column(db.Integer(), db.ForeignKey("perfil_manutentor.id"), nullable=False)

    tiposituacaoordem = db.relationship("TipoSituacaoOrdem", back_populates="tiposituacaoordemperfilmanutentor")
    perfilmanutentor = db.relationship("PerfilManutentor", back_populates="tiposituacaoordemperfilmanutentor")

    def __repr__(self) -> str:
        return f'<TipoSituacaoOrdemPerfilManutentor: {self.id}-{self.tiposituacaoordem.nome}-{self.perfilmanutentor.nome}>'


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
    observacao = db.Column(db.String(200), nullable=True)

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
        """Função para alterar os atributos"""
        self.ordemservico_id = ordem_id
        self.tiposituacaoordem_id = tipo_situacao_id
        self.usuario_id = current_user.id
        self.data = datetime.datetime.now()

        # Criando o objeto OrdemServiço
        ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
        # Alterando para a situação da tramitação
        ordem.tiposituacaoordem_id = tipo_situacao_id

        # Cria um objeto SituacaoOrdem
        situacao = TipoSituacaoOrdem.query.filter_by(id=tipo_situacao_id).one_or_none()

        # Alterando o status do ordem
        if situacao.sigla in ["CONC", "CANC", "REPR"]:
            sigla = situacao.sigla
            if situacao.sigla == "REPR":
                sigla = "PEND"
                ordem.reservico = True

            status = TipoStatusOrdem.query.filter_by(sigla=sigla).one_or_none()
            ordem.tipostatusordem_id = status.id

        # Gera um incremento no tempo para que as tramitações fiquem na ordem
        if situacao.sigla in ["AGAP", "AGFI", "ENCE"]:
            self.data = datetime.datetime.now() + datetime.timedelta(seconds=1)

        # Verifica estara aguardando fiscalização dará por encerrada
        if situacao.sigla == "ENCE":
            # Caso seja, colocará a data de fechamento da OrdemServico
            ordem.data_fechamento = datetime.datetime.now()

        if ordem.salvar():
            flash("Ordem de Serviço Atualizada", category="success")
        else:
            flash("Erro ao atualizar a Ordem de Serviço", category="success")

    def alterar_observacao(self, form_listaatividade, tiposituacao: [TipoSituacaoOrdem]):
        """Função que altera o campo observação da tramitação"""
        if tiposituacao.sigla in ["AGSE", "AGMT", "PARA", "CANC", "REPR"]:
            self.observacao = form_listaatividade.observacao.data.upper()
        else:
            self.observacao = tiposituacao.nome

    @staticmethod
    def insere_tramitacao(descricao, texto):
        tramitacao = TramitacaoOrdem()

        ordem = OrdemServico.query.filter_by(descricao=descricao).order_by(OrdemServico.id.desc()).first()
        tiposituacao = TipoSituacaoOrdem.query.filter_by(sigla='AGAP').one_or_none()

        tramitacao.ordemservico_id = ordem.id
        tramitacao.usuario_id = current_user.id
        tramitacao.tiposituacaoordem_id = tiposituacao.id
        tramitacao.observacao = texto
        tramitacao.data = datetime.datetime.now()
        tramitacao.salvar()


class OrdemServico(db.Model):
    titulos_csv = {'codigo; descricao; data_abertura; data_prevista; data_fechamento; equipamento_descricao_curta;'
                   'situacao_nome; status_nome; solicitante_nome; tipo_ordem_nome; plano_manutencao_codigo; reservico'}

    __tablename__ = 'ordem_servico'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    codigo = db.Column(db.Integer())
    descricao = db.Column(db.String(100), nullable=False, index=True)
    data_abertura = db.Column(db.DateTime(), nullable=False)
    data_prevista = db.Column(db.DateTime(), nullable=True)
    data_fechamento = db.Column(db.DateTime(), nullable=True)

    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    tiposituacaoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_situacao_ordem.id"), nullable=False)
    tipostatusordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_status_ordem.id"), nullable=False)
    solicitante_id = db.Column(db.Integer(), db.ForeignKey("usuario.id"), nullable=True)
    tipoordem_id = db.Column(db.Integer(), db.ForeignKey("tipo_ordem.id"), nullable=False)
    planomanutencao_id = db.Column(db.Integer(), nullable=True)
    listaatividade_id = db.Column(db.Integer(), db.ForeignKey("lista_atividade.id"), nullable=True)
    reservico = db.Column(db.Boolean, default=False)

    equipamento = db.relationship("Equipamento", back_populates="ordemservico")
    tiposituacaoordem = db.relationship("TipoSituacaoOrdem", back_populates="ordemservico")
    tipostatusordem = db.relationship("TipoStatusOrdem", back_populates="ordemservico")
    usuario = db.relationship("Usuario", back_populates="ordemservico")
    tipoordem = db.relationship("TipoOrdem", back_populates="ordemservico")
    tramitacaoordem = db.relationship("TramitacaoOrdem", back_populates="ordemservico", cascade="all, delete-orphan")
    listaatividade = db.relationship("ListaAtividade", back_populates="ordemservico", cascade="all, delete-orphan",
                                     single_parent=True)

    def __repr__(self) -> str:
        return f'{self.codigo};{self.descricao};{self.data_abertura};{self.data_prevista};{self.data_fechamento};' \
               f'{self.equipamento.descricao_curta};{self.tiposituacaoordem.nome};{self.tipostatusordem.nome};' \
               f'{atributo_existe(self, "usuario", "nome")};{self.tipoordem.nome};' \
               f'{PlanoManutencao.retornar_codigo_plano(self.planomanutencao_id)};{self.reservico}'

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
            self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("AGAP")
            self.tipostatusordem_id = TipoStatusOrdem.retornar_id_status("PEND")
            self.tipoordem_id = form.tipo.data
            self.descricao = form.descricao.data.upper()
            self.equipamento_id = form.equipamento.data

    def alterar_atributos_by_plano(self, plano):
        """     Função para atribuir valores para ordem a partir de um plano de manutenção  """
        self.codigo = OrdemServico.gerar_codigo_ordem()
        self.data_abertura = datetime.datetime.now()
        self.solicitante_id = None
        self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("AGAP")
        self.tipostatusordem_id = TipoStatusOrdem.retornar_id_status("PEND")
        self.tipoordem_id = plano.tipoordem_id
        self.descricao = plano.nome
        self.equipamento_id = plano.equipamento_id
        self.planomanutencao_id = plano.id
        self.data_prevista = plano.data_inicio
        self.listaatividade_id = plano.listaatividade_id
        ListaAtividade.copiar_lista(plano.listaatividade_id)

    def alterar_atributos_by_ordem(self, ordem, plano):
        self.codigo = OrdemServico.gerar_codigo_ordem()
        self.data_abertura = datetime.datetime.now()
        self.solicitante_id = None
        self.tiposituacaoordem_id = TipoSituacaoOrdem.retornar_id_situacao("AGAP")
        self.tipostatusordem_id = TipoStatusOrdem.retornar_id_status("PEND")
        self.tipoordem_id = ordem.tipoordem_id
        self.descricao = ordem.descricao
        self.equipamento_id = ordem.equipamento_id
        self.planomanutencao_id = ordem.planomanutencao_id
        self.data_prevista = plano.data_inicio
        self.listaatividade_id = ListaAtividade.copiar_lista(plano.listaatividade_id)

    @staticmethod
    def gerar_codigo_ordem():
        """Função para retornar o número para a proxima OS"""
        return db.session.query(func.max(OrdemServico.codigo)).first()[0] + 1

    @staticmethod
    def verificar_ordem_perfil_manutentor():
        resultado = False

        if TipoSituacaoOrdemPerfilManutentor.query.filter(
                TipoSituacaoOrdemPerfilManutentor.perfilmanutentor_id == PerfilManutentorUsuario.perfilmanutentor_id,
                PerfilManutentorUsuario.usuario_id == current_user.id,
                TipoSituacaoOrdemPerfilManutentor.tiposituacaoordem_id == OrdemServico.tiposituacaoordem_id).count() > 0:
            resultado = True

        return resultado
