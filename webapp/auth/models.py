from webapp.auth import bcrypt, AnonymousUserMixin, jwt
from webapp import db
from webapp.company.models import Company
from webapp.plan.models import View
from flask_jwt_extended import create_access_token, get_jwt_identity
import jwt
import datetime
import config


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(50))
    # user = db.relationship("User", back_populates="role")
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="role")
    viewrole = db.relationship("ViewRole", back_populates="role")

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def change_attributes(self, form):
        self.name = form.name.data
        self.description = form.description.data
        self.company_id = form.company.data


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))
    confirmed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime(), nullable=True)
    last_seen = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer(), nullable=False)

    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_role_name(self):
        role = Role.query.filter_by(id=self.role_id).first()
        return role.name

    def get_company_name(self):
        company = Company.query.filter_by(id=self.company_id).first()
        return company.name

    # # @cache.memoize(60)
    def has_view(self, name):
        for viewrole in ViewRole.query.filter_by(role_id=self.role_id).all():
            view = View.query.filter_by(id=viewrole.view_id).one()
            if view.name == name:
                return True
        return False

    def get_id(self):
        return str(self.id)

    def set_email(self, email):
        self.email = email

    def set_confirmed(self, confirmed):
        self.confirmed = confirmed
        self.member_since = datetime.datetime.now()

    def set_password(self, password):
        # self.password = bcrypt.generate_password_hash(password)
        self.password = password

    def set_active(self, active):
        self.active = active

    def check_password(self, password):
        # return bcrypt.check_password_hash(self.password, password)
        return self.password == password

    def ping(self):
        self.last_seen = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def create_token(self, expiration=60):
        token = jwt.encode(
            {"id": self.id,
             "email": self.email,
             "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=expiration)},
            config.Config.SECRET_KEY,
            algorithm="HS256"
        )
        return token

    @staticmethod
    def verify_token(tipo, token):
        try:
            data = jwt.decode(
                token,
                config.Config.SECRET_KEY,
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False, 0
        return True, data.get(tipo)

    def change_attributes(self, form, new=False):
        self.username = form.username.data
        self.email = form.email.data
        self.company_id = form.company.data
        self.role_id = form.role.data
        self.active = form.active.data
        self.password = '12345678'
        self.confirmed = True
        if new:
            self.member_since = datetime.datetime.now()

    def change_active(self):
        if self.active:
            self.set_active(False)
        else:
            self.set_active(True)

    def get_views_role(self):
        user = User.query.filter_by(username=self.username).one()
        viewroles = ViewRole.query.filter_by(role_id=user.role_id, active=True).all()

        views = []
        for viewrole in viewroles:
            view = View.query.filter_by(id=viewrole.view_id).one()
            views.append(dict(name=view.name, url=view.url, icon=view.icon))
        return views


class ViewRole(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))
    role = db.relationship("Role", back_populates="viewrole")
    view_id = db.Column(db.Integer(), db.ForeignKey("view.id"))
    view = db.relationship("View", back_populates="viewrole")

    def __repr__(self):
        return '<ViewRole {}>'.format(self.id)

    def change_attributes(self, form):
        self.role_id = form.user.data
        self.view_id = form.view.data

    def get_name_view(self, id):
        view = View.query.filter_by(id=id).first()
        return view.get_name()

    def change_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True
