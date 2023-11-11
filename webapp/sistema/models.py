from flask_login import current_user

from webapp import db
from webapp.utils.tools import data_atual_utc
from webapp.utils.objetos import salvar


class LogsEventos(db.Model):
    """    Classe de tipos de datas (data fixa/móvel)   """
    __tablename__ = 'logs_eventos'
    id = db.Column(db.Integer(), primary_key=True)
    data = db.Column(db.DateTime(), nullable=True)
    tipo = db.Column(db.String(10), nullable=True)
    funcao_nome = db.Column(db.String(50), nullable=True)
    empresa_id = db.Column(db.Integer, nullable=True)
    usuario_nome = db.Column(db.String(50), nullable=True)
    argumento = db.Column(db.String(200), nullable=True)

    def __repr__(self) -> str:
        return f'logevento: {self.id}-{self.data}-{self.tipo}-{self.funcao_nome}-{self.empresa_id}-{self.usuario_nome}'

    @staticmethod
    def registrar(tipo, funcao, **kwargs):
        """Função que monta o objeto evento e salve no BD"""
        # concatena as chaves-valor
        kwargs_str = ", ".join([f"{key}={value}" for key, value in kwargs.items()])
        # monta o objeto evento
        logevento = LogsEventos(data=data_atual_utc(),
                                tipo=tipo.upper(),
                                funcao_nome=funcao.upper(),
                                empresa_id=current_user.empresa_id,
                                usuario_nome=current_user.nome.upper(),
                                argumento=kwargs_str
                                )
        # salva no BD
        salvar(logevento)
