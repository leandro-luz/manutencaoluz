import re
from flask import flash
from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField, ValidationError, DateField, \
    FileField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Optional

from webapp.empresa.models import Interessado, Empresa
from datetime import datetime


def cnpj_validate(form, field):
    if not re.match(r"([0-9]{2}[.]?[0-9]{3}[.]?[0-9]{3}[/]?[0-9]{4}[-]?[0-9]{2})", field.data):
        flash("Formato do cnpj válido: xx.xxx.xxx/xxxx-xx", category="danger")
        raise ValidationError("Formato cnpj inválido")


class EmpresaForm(Form):
    """    Formulário de da classe empresa    """
    id = IntegerField('Id')
    razao_social = StringField('Razão Social', validators=[InputRequired(), Length(max=50)],
                               render_kw={"placeholder": "Digite a Razão Social da empresa"})
    cnpj = StringField('Cnpj', validators=[InputRequired(), Length(min=14, max=18), cnpj_validate],
                       render_kw={"placeholder": "xx.xxx.xxx/xxxx-xx"})
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "email@dominio.com"})
    telefone = StringField('Telefone', validators=[InputRequired()],
                           render_kw={"placeholder": "(xx)x xxxx-xxxx"})
    cep = StringField('Cep',
                      validators=[InputRequired(), Length(min=8, max=10, message="O CEP está no formato errado")],
                      render_kw={"placeholder": "xxxxxxxxx"})
    numero = IntegerField('Número', validators=[InputRequired(), NumberRange(min=0)],
                          render_kw={"placeholder": "Digite o número"})
    complemento = StringField('Complemento', render_kw={"placeholder": "Digite o complemento"})
    logradouro = StringField('Logradouro', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite o logradouro"})
    bairro = StringField('Bairro', validators=[InputRequired()], render_kw={"placeholder": "Digite o bairro"})
    municipio = StringField('Município', validators=[InputRequired()], render_kw={"placeholder": "Digite o município"})
    uf = StringField('UF', validators=[InputRequired()], render_kw={"placeholder": "Digite o UF"})
    localizacao = StringField('Localização', render_kw={"placeholder": "Digite as coordenadas"})

    ativo = BooleanField('Ativo')

    nome_fantasia = StringField('Nome Fantasia', validators=[InputRequired()],
                                render_kw={"placeholder": "Digite o nome fantasia"})
    data_abertura = DateField('Data de Abertura', format='%Y-%m-%d', validators=[InputRequired()],
                              render_kw={"placeholder": "Digite de criação do cnpj"})
    situacao = StringField('Situação', render_kw={"placeholder": "Digite a situação do cnpj"})
    tipo = StringField('Tipo', validators=[InputRequired()], render_kw={"placeholder": "Matriz/Filial"})
    nome_responsavel = StringField('Nome do Responsável', render_kw={"placeholder": "Digite o nome do responsável"})
    porte = StringField('Porte', render_kw={"placeholder": "Digite o porte da empresa"})
    natureza_juridica = StringField('Natureza Jurídica', render_kw={"placeholder": "Digite a natureza jurídica"})
    cnae_principal = StringField('CNAE P - Código', render_kw={"placeholder": "XX.XX-X-XX"})
    cnae_principal_texto = StringField('CNAE P - Texto', render_kw={"placeholder": "Digite o texto do cnae principal"})

    inscricao_estadual = StringField('Inscrição Estadual', render_kw={"placeholder": "Digite a inscrição estadual"})
    inscricao_municipal = StringField('Inscrição Municipal', render_kw={"placeholder": "Digite a inscrição municipal"})

    contrato = SelectField('Contrato', choices=[], validators=[InputRequired()], coerce=int)
    enviar_email = BooleanField('Enviar Email?')

    file = FileField('Escolha um arquivo para o cadastro de empresas em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(EmpresaForm, self).validate()

        # instância uma empresa com as informações sem alterações, com base no identificador
        empresa = Empresa.query.filter_by(id=self.id.data).one_or_none()

        if check_validate:
            # verifica se existe empresa com o mesmo razao_social, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id,
                                               Empresa.razao_social == self.razao_social.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.razao_social.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa com este razao_social", category="danger")
                return False

            # verifica se existe empresa com o mesmo cnpj, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id, Empresa.cnpj == self.cnpj.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.cnpj.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa com este cnpj", category="danger")
                return False

            # Verifica se o cnpj está válido
            if not Empresa.validar_cnpj(self.cnpj.data):
                flash("O CNPJ informado não está válido", category="danger")
                return False

            # verifica se existe empresa com o mesmo endereço eletrônico, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id,
                                               Empresa.email == self.email.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.email.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa vinculada a este email", category="danger")
                return False

            if self.contrato.data == 0:
                flash("Não informado o contrato para a empresa", category="danger")
                return False

            return True
        else:
            return False


class EmpresaSimplesForm(Form):
    """    Formulário de da classe empresa    """
    id = IntegerField('Id')
    nome_fantasia = StringField('Nome Fantasia', validators=[InputRequired()],
                                render_kw={"placeholder": "Digite o nome fantasia"})
    cnpj = StringField('Cnpj', validators=[InputRequired(), Length(min=14, max=18), cnpj_validate],
                       render_kw={"placeholder": "xx.xxx.xxx/xxxx-xx"})
    cep = StringField('Cep', validators=[InputRequired(), Length(min=8, max=8, message="O CEP está no formato errado")],
                      render_kw={"placeholder": "xxxxxxxxx"})
    numero = IntegerField('Número', validators=[InputRequired(), NumberRange(min=0)],
                          render_kw={"placeholder": "Digite o número"})
    complemento = StringField('Complemento', render_kw={"placeholder": "Digite o complemento"})
    logradouro = StringField('Logradouro', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite o logradouro"})
    bairro = StringField('Bairro', validators=[InputRequired()], render_kw={"placeholder": "Digite o bairro"})
    municipio = StringField('Município', validators=[InputRequired()], render_kw={"placeholder": "Digite o município"})
    uf = StringField('UF', validators=[InputRequired()], render_kw={"placeholder": "Digite o UF"})
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "email@dominio.com"})
    telefone = StringField('Telefone', validators=[InputRequired()],
                           render_kw={"placeholder": "(xx)x xxxx-xxxx"})
    contrato = SelectField('Contrato', choices=[], validate_choice=False, coerce=int)

    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(EmpresaSimplesForm, self).validate()

        # instância uma empresa com as informações sem alterações, com base no identificador
        empresa = Empresa.query.filter_by(id=self.id.data).one_or_none()

        if check_validate:
            # verifica se existe empresa com o mesmo razao_social, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id,
                                               Empresa.razao_social == self.nome_fantasia.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.nome_fantasia.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa com este Nome Fantasia", category="danger")
                return False

            # verifica se existe empresa com o mesmo cnpj, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id, Empresa.cnpj == self.cnpj.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.cnpj.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa com este cnpj", category="danger")
                return False

            # Verifica se o cnpj está válido
            if not Empresa.validar_cnpj(self.cnpj.data):
                flash("O CNPJ informado não está válido", category="danger")
                return False

            # verifica se existe empresa com o mesmo endereço eletrônico, ignorando a empresa repassada(se <> 0)
            if empresa:
                empresa = Empresa.query.filter(Empresa.id != empresa.id,
                                               Empresa.email == self.email.data).one_or_none()
            else:
                empresa = Empresa.query.filter(Empresa.razao_social == self.email.data).one_or_none()

            if empresa:
                flash("Já existe uma empresa vinculada a este email", category="danger")
                return False
            return True

        else:
            return False


class RegistroInteressadoForm(Form):
    nome_fantasia = StringField('Nome Fantasia', [InputRequired(), Length(max=50)],
                                render_kw={"placeholder": "Digite a Razão Social da empresa"})
    cnpj = StringField('Cnpj', validators=[InputRequired(), Length(min=18, max=18), cnpj_validate],
                       render_kw={"placeholder": "00.000.000/0000-00"})
    email = StringField('Email', [InputRequired(), Email()],
                        render_kw={"placeholder": "email@domínio.com"})
    telefone = StringField('Telefone', [InputRequired(), Length(max=20)],
                           render_kw={"placeholder": "(00) 0 0000-0000"})

    submit = SubmitField('Solicitar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(RegistroInteressadoForm, self).validate()

        if check_validate:
            # verifica se o razao_social da empresa já foi solicitado
            interessado = Interessado.query.filter_by(nome_fantasia=self.nome_fantasia.data).first()
            if interessado:
                flash("Já foi solicitado acesso para esta empresa", category="danger")
                return False
            # verifica se o cnpj já foi solicitado
            interessado = Interessado.query.filter_by(cnpj=self.cnpj.data).first()
            if interessado:
                flash("Já foi solicitado acesso com este cnpj", category="danger")
                return False
            return True
        else:
            return False
