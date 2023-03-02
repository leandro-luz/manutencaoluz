from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, Email, NumberRange
from webapp.company.models import Company, Business, Subbusiness
from flask import flash
import re


def cnpj_validate(form, field):
    if not re.match(r"([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[/]?[0-9]{4}[-]?[0-9]{2})", field.data):
        flash("Formato do cnpj válido: xx.xxx.xxx/xxxx-xx", category="danger")
        raise ValidationError("Formato cnpj inválido")


class CompanyForm(Form):
    """    Formulário de da classe empresa    """
    id = IntegerField('Id')
    name = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome da empresa"})
    cnpj = StringField('Cnpj', validators=[InputRequired(), Length(min=18, max=18), cnpj_validate],
                       render_kw={"placeholder": "Digite o cnpj"})
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o email"})
    cep = StringField('Cep', validators=[InputRequired(), Length(min=8, max=8)],
                      render_kw={"placeholder": "Digite o cep"})

    numero = IntegerField('Número', validators=[InputRequired(), NumberRange(min=0)],
                          render_kw={"placeholder": "Digite o número"})
    complemento = StringField('Complemento',
                              render_kw={"placeholder": "Digite o complemento"})
    logradouro = StringField('Logradouro', validators=[InputRequired()])
    bairro = StringField('Bairro', validators=[InputRequired()])
    municipio = StringField('Município', validators=[InputRequired()])
    uf = StringField('UF', validators=[InputRequired()])

    active = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a empresa está ativa"})
    business = SelectField('Ramo de Negócio', choices=[], validate_choice=False, coerce=int)
    subbusiness = SelectField('Sub-Ramo de Negócio', choices=[], validate_choice=False, coerce=int)
    plan = SelectField('Plano', choices=[], validate_choice=False, coerce=int)

    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(CompanyForm, self).validate()

        # instância uma empresa com as informações sem alterações, com base no identificador
        company_ = Company.query.filter_by(id=self.id.data).one_or_none()

        if check_validate:
            # verifica se existe empresa com o mesmo nome, ignorando a empresa repassada(se <> 0)
            if company_:
                company = Company.query.filter(Company.id != company_.id, Company.name == self.name.data).one_or_none()
            else:
                company = Company.query.filter(Company.name == self.name.data).one_or_none()

            if company:
                flash("Já existe uma empresa com este nome", category="danger")
                return False

            # verifica se existe empresa com o mesmo cnpj, ignorando a empresa repassada(se <> 0)
            if company_:
                company = Company.query.filter(Company.id != company_.id, Company.cnpj == self.cnpj.data).one_or_none()
            else:
                company = Company.query.filter(Company.name == self.cnpj.data).one_or_none()

            if company:
                flash("Já existe uma empresa com este cnpj", category="danger")
                return False

            # verifica se existe empresa com o mesmo endereço eletronico, ignorando a empresa repassada(se <> 0)
            if company_:
                company = Company.query.filter(Company.id != company_.id,
                                               Company.email == self.email.data).one_or_none()
            else:
                company = Company.query.filter(Company.name == self.email.data).one_or_none()

            if company:
                flash("Já existe uma empresa vinculada a este email", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Empresa não válidada", category="danger")
            return False

        return True


class BusinessForm(Form):
    name = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do ramo de negócios"})
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs) -> bool:
        """    Função que válida as informações do formulário    """
        check_validate = super(BusinessForm, self).validate()  # valida de forma inicial as informações

        if check_validate:  # checa a validação inicial
            # instância um negócio com base no identificador
            business = Business.query.filter_by(name=self.name.data).one_or_none()

            if business:  # se existe deve gerar uma falha
                flash(f'Já existe um Negócio com este nome "{self.name.data}"', category="danger")
                return False
        else:
            flash("Negócio não válidado", category="danger")
            return False

        return True


class SubbusinessForm(Form):
    name = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do sub-ramo de negócios"})
    business = SelectField('Ramo de Negócio', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs) -> bool:
        """    Função que válida as informações do formulário    """
        check_validate = super(SubbusinessForm, self).validate()  # valida de forma inicial as informações

        if check_validate:  # checa a validação inicial
            # instância um subnegócio com base no identificador
            subbusiness = Subbusiness.query.filter_by(name=self.name.data, business_id=self.business.data).one_or_none()

            if subbusiness:  # se existe deve gerar uma falha
                flash(f'Já existe um Subnegócio com este nome "{self.name.data}"', category="danger")
                return False
        else:
            flash("Subnegócio não válidado", category="danger")
            return False

        return True
