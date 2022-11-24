from webapp import db
from webapp.plan.models import Plan
import datetime


class Business(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    subbusiness = db.relationship("Subbusiness", back_populates="business")

    def __repr__(self):
        return '<Business {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data


class Subbusiness(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=False)
    business_id = db.Column(db.Integer(), db.ForeignKey("business.id"))
    business = db.relationship("Business", back_populates="subbusiness")
    company = db.relationship("Company", back_populates="subbusiness")

    def __repr__(self):
        return '<SubBusiness {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data
        self.business_id = form.business.data


class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    cnpj = db.Column(db.Integer(), nullable=False, unique=True)
    cep = db.Column(db.Integer(), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    manager_company_id = db.Column(db.Integer(), nullable=False)
    subbusiness_id = db.Column(db.Integer(), db.ForeignKey("subbusiness.id"))
    subbusiness = db.relationship("Subbusiness", back_populates="company")
    plan_id = db.Column(db.Integer(), db.ForeignKey("plan.id"))
    plan = db.relationship("Plan", back_populates="company")

    user = db.relationship("User", back_populates="company")
    role = db.relationship("Role", back_populates="company")
    asset = db.relationship("Asset", back_populates="company")
    group = db.relationship("Group", back_populates="company")
    supplier = db.relationship("Supplier", back_populates="company")

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def __init__(self, name=""):
        self.business_id = Subbusiness.query.filter_by(name="teste").one()
        self.name = name

    def change_attributes(self, form, company_id, new=False):
        self.name = form.name.data
        self.cnpj = form.cnpj.data
        self.cep = form.cep.data
        self.email = form.email.data
        self.active = form.active.data
        self.subbusiness_id = form.subbusiness.data
        self.plan_id = form.plan.data
        self.manager_company_id = company_id
        if new:
            self.member_since = datetime.datetime.now()


    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def get_name_plan(self):
        plan = Plan.query.filter_by(id=self.plan_id).one()
        return plan.get_name()

