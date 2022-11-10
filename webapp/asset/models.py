from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt
import datetime
import config


class Type(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="type")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Type {}>'.format(self.name)


class Asset(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cod = db.Column(db.String(50), nullable=True)
    short_description = db.Column(db.String(50), nullable=True)
    long_description = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    ns = db.Column(db.String(50), nullable=True)
    dimension_x = db.Column(db.Integer(), nullable=True)
    dimension_y = db.Column(db.Integer(), nullable=True)
    dimension_z = db.Column(db.Integer(), nullable=True)
    weight = db.Column(db.Integer(), nullable=True)
    year_manufacture = db.Column(db.DateTime(), nullable=True)
    date_acquisition = db.Column(db.DateTime(), nullable=True)
    date_installation = db.Column(db.DateTime(), nullable=True)
    cost_acquisition = db.Column(db.Integer(), nullable=True)
    depreciation = db.Column(db.Integer(), nullable=True)
    tag = db.Column(db.Integer(), nullable=True)
    cost_center = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean, default=True)
    type_id = db.Column(db.Integer(), nullable=True)

    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="asset")

    def __repr__(self):
        return '<Asset {}>'.format(self.name)

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def change_attributes(self, form, new):
        self.cod = form.cod.data
        self.short_description = form.short_description.data
        self.long_description = form.long_description.data
        self.manufacturer = form.manufacturer.data
        self.brand = form.brand.data
        self.model = form.model.data
        self.ns = form.ns.data
        self.dimension_x = form.dimension_x.data
        self.dimension_y = form.dimension_y.data
        self.dimension_z = form.dimension_z.data
        self.weight = form.weight.data
        self.year_manufacture = form.year_manufacture.data
        self.date_acquisition = form.date_acquisition.data
        self.date_installation = form.date_installation.data
        self.cost_acquisition = form.cost_acquisition.data
        self.depreciation = form.depreciation.data
        self.tag = form.tag.data
        self.cost_center = form.cost_center.data
        self.active = form.active.data
        self.type_id = form.type_id.data
        self.company_id = form.company.data

    def change_active(self):
        if self.active:
            self.set_active(False)
        else:
            self.set_active(True)
