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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Subbusiness(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=False)
    business_id = db.Column(db.Integer(), db.ForeignKey("business.id"))
    business = db.relationship("Business", back_populates="subbusiness")
    company = db.relationship("Company", back_populates="subbusiness")

    def __repr__(self):
        return '<SubBusiness {}>'.format(self.name)


class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True, unique=True)
    cnpj = db.Column(db.Integer(), nullable=False, index=True, unique=True)
    cep = db.Column(db.Integer(), nullable=False, index=True, unique=False)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    active = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    subbusiness_id = db.Column(db.Integer(), db.ForeignKey("subbusiness.id"))
    subbusiness = db.relationship("Subbusiness", back_populates="company")
    user = db.relationship("User", back_populates="company")

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def __init__(self, name=""):
        self.business_id = Subbusiness.query.filter_by(name="teste").one()
        self.name = name

    def setName(self, name):
        self.name = name

    def setCnpj(self, cnpj):
        self.cnpj = cnpj

    def setCep(self, cep):
        self.cep = cep

    def setEmail(self, email):
        self.email = email

    def setActive(self, active):
        self.active = active

    def setSubbsiness(self, id):
        self.subbusiness_id = id

    def setMemberSince(self):
        self.member_since = datetime.datetime.now()

    def getName(self):
        return self.name

    def getCnpj(self):
        return self.cnpj

    def getCep(self):
        return self.cep

    def getEmail(self):
        return self.email

    def getActive(self):
        return self.active

    def getSubbsiness(self):
        return self.subbusiness_id

    def getMemberSince(self):
        return self.member_since

    def changeActive(self):
        if self.active:
            self.setActive(False)
        else:
            self.setActive(True)
