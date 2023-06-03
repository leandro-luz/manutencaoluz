import logging
from webapp import db

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
    __tablename__ = 'plano_manutencao'
    """    Classe de Plano de Manutenção   """
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, index=True)
    codigo = db.Column(db.String(50), nullable=False, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    tipodata_id = db.Column(db.Integer(), db.ForeignKey("tipo_data.id"), nullable=False)
    periodicidade_id = db.Column(db.Integer(), db.ForeignKey("periodicidade.id"), nullable=False)
    equipamento_id = db.Column(db.Integer(), db.ForeignKey("equipamento.id"), nullable=False)
    empresa_id = db.Column(db.Integer(), nullable=False)

    tipodata = db.relationship("TipoData", back_populates="planomanutencao")
    periodicidade = db.relationship("Periodicidade", back_populates="planomanutencao")
    equipamento = db.relationship("Equipamento", back_populates="planomanutencao")
    # ordemservico = db.relationship("OrdemServico", back_populates="planomanutencao")


    def __repr__(self):
        return f'<Plano de Manutenção: {self.id}-{self.codigo}>'

    def alterar_atributos(self, form):
        """    Função para alterar os atributos do objeto    """
        self.codigo = form.codigo.data
        self.ativo = form.ativo.data
        self.tipodata_id = form.tipodata.data
        self.periodicidade_id = form.periodicidade.data
        self.equipamento_id = form.equipamento.data

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
