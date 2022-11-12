from webapp import db


class Supplier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="supplier")

    def __repr__(self):
        return '<Supplier {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data
        self.company_id = form.company.data
