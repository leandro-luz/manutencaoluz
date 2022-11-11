from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, SelectField, \
    PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from .models import Company
from flask import flash


class CompanyForm(Form):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome da empresa"})
    cnpj = IntegerField('Cnpj', validators=[DataRequired()],
                        render_kw={"placeholder": "Digite o cnpj"})
    cep = IntegerField('Cep', validators=[DataRequired()],
                       render_kw={"placeholder": "Digite o cep"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Digite o email"})
    active = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a empresa está ativa"})
    business = SelectField('Ramo de Negócio', choices=[], coerce=int)
    subbusiness = SelectField('Sub-Ramo de Negócio', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        # flash("Empresa não adicionada", category="danger")
        return True


class BusinessForm(Form):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do ramo de negócios"})
    submit = SubmitField("Cadastrar")

    def validate(self):
        return True


class SubbusinessForm(Form):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do sub-ramo de negócios"})
    business = SelectField('Ramo de Negócio', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        return True
