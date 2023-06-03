from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length
from flask import flash
from webapp.contrato.models import Contrato, Telacontrato


class ContratoFomr(Form):
    """    Classe do formulário de contrato de assinaturas    """
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do contrato"})
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs) -> bool:
        """        Função que válida as informações do formulário        """
        check_validate = super(ContratoFomr, self).validate()  # valida de forma inicial as informações

        if check_validate:  # checa a validação inicial
            # busca se existe algum contrato com o nome
            plan = Contrato.query.filter_by(nome=self.nome.data).one_or_none()

            if plan:  # se existe deve gerar uma falha
                flash(f'Já existe um Contrato de Assinatura com este nome "{self.nome.data}"', category="danger")
                return False
        else:
            flash("Contrato de Assinatura não válidado", category="danger")
            return False

        return True


class TelaContratoForm(Form):
    """    Formulário o relacionamento Contrato de assinatura e Telas    """
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    contrato = SelectField('Contrato', choices=[], validate_choice=False, coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(TelaContratoForm, self).validate()  # válida inicialmente as informações

        if check_validate:
            telacontrato = Telacontrato.query.filter_by(contrato_id=self.contrato.data, tela_id=self.tela.data).one_or_none()
            if telacontrato:
                flash("Tela já registrada para este contrato", category="danger")
                return False
        else:
            return False

        return True


class TelaForm(Form):
    """    Formulário das Telas    """
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome da tela"})
    icon = StringField('Icone', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do icone"})
    url = StringField('URL', validators=[InputRequired(), Length(max=50)],
                      render_kw={"placeholder": "Digite o endereço da url"})
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        # if our validators do not pass
        # check_validate = super(EmpresaForm, self).validate()
        # if not check_validate:
        #     return False

        # flash("Empresa não adicionada", category="danger")
        return True