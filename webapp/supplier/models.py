from webapp import db


class Supplier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

    company_id = db.Column(db.Integer(), db.ForeignKey("empresa.id"), nullable=False)

    empresa = db.relationship("Empresa", back_populates="supplier")

    def __repr__(self):
        return f'<Supplier {self.nome}>'
