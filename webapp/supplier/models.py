import logging
from webapp import db

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


class Supplier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    company_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="supplier")

    def __repr__(self):
        return f'<Supplier {self.nome}>'

    def change_attributes(self, form):
        self.nome = form.nome.data
        self.company_id = form.company.data

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False
