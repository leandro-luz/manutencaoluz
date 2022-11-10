from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt
import datetime
import config


class Supplier(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    # company = db.relationship("Company", back_populates="supplier")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Supplier {}>'.format(self.name)