from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange
from flask import flash
from webapp.contrato.models import Contrato, Telacontrato


class ContratoForm(Form):
    """    Classe do formulário de contrato de assinaturas    """
    id = IntegerField('id')
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do contrato"})
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    ativo = BooleanField('Ativo')
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs) -> bool:
        """        Função que válida as informações do formulário        """
        check_validate = super(ContratoForm, self).validate()  # valida de forma inicial as informações

        if check_validate:  # checa a validação inicial
            # busca se existe algum contrato com o nome
            if Contrato.query.filter(Contrato.id != self.id.data,
                                     Contrato.nome == self.nome.data).one_or_none():
                flash(f'Já existe um Contrato com este nome "{self.nome.data}"', category="danger")
                return False
        else:
            flash("Contrato não válidado", category="danger")
            return False

        return True


class TelaContratoForm(Form):
    """    Formulário o relacionamento Contrato de assinatura e Telas    """
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(TelaContratoForm, self).validate()  # válida inicialmente as informações

        if not check_validate:
            # telacontrato = Telacontrato.query.filter_by(contrato_id=self.contrato.data,
            #                                             tela_id=self.tela.data).one_or_none()
            # if telacontrato:
            #     flash("Tela já registrada para este contrato", category="danger")
            return False
            #     return False

        return True


class TelaForm(Form):
    """    Formulário das Telas    """
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome da tela"})
    icon = StringField('Icone', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do icone"})
    url = StringField('URL', validators=[InputRequired(), Length(max=50)],
                      render_kw={"placeholder": "Digite o endereço da url"})
    posicao = IntegerField('Posição', validators=[InputRequired(), NumberRange(min=0)],
                           render_kw={"placeholder": "Digite a posição"})

    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        # if our validators do not pass
        # check_validate = super(EmpresaForm, self).validate()
        # if not check_validate:
        #     return False

        # flash("Empresa não adicionada", category="danger")
        return True
