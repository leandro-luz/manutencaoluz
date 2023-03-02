from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, SelectField, \
    PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
from .models import Supplier
from flask import flash


class SupplierForm(Form):
    name = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do sub-ramo de negócios"})
    company = SelectField('Empresa', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        return True
