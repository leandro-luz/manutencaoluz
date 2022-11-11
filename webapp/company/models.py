from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt
import datetime
import config


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
    subbusiness_id = db.Column(db.Integer(), db.ForeignKey("subbusiness.id"))

    subbusiness = db.relationship("Subbusiness", back_populates="company")
    user = db.relationship("User", back_populates="company")
    role = db.relationship("Role", back_populates="company")
    asset = db.relationship("Asset", back_populates="company")
    type = db.relationship("Type", back_populates="company")

    # supplier = db.relationship("Supplier", back_populates="company")

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def __init__(self, name=""):
        self.business_id = Subbusiness.query.filter_by(name="teste").one()
        self.name = name

    def change_attributes(self, form, new=False):
        self.name = form.name.data
        self.cnpj = form.cnpj.data
        self.cep = form.cep.data
        self.email = form.email.data
        self.active = form.active.data
        self.subbusiness_id = form.subbusiness.data
        if new:
            self.member_since = datetime.datetime.now()

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True
