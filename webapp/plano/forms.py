from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import InputRequired, Length
from flask import flash
from webapp.plano.models import Plano, Telaplano


class PlanoForm(Form):
    """    Classe do formulário de plano de assinaturas    """
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do plano"})
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs) -> bool:
        """        Função que válida as informações do formulário        """
        check_validate = super(PlanoForm, self).validate()  # valida de forma inicial as informações

        if check_validate:  # checa a validação inicial
            plan = Plano.query.filter_by(nome=self.nome.data).one_or_none()  # busca se existe algum plano com o nome

            if plan:  # se existe deve gerar uma falha
                flash(f'Já existe um Plano de Assinatura com este nome "{self.nome.data}"', category="danger")
                return False
        else:
            flash("Plano de Assinatura não válidado", category="danger")
            return False

        return True


class TelaPlanoForm(Form):
    """    Formulário o relacionamento Plano de assinatura e Telas    """
    tela = SelectField('Telas', choices=[], validate_choice=False, coerce=int)
    plano = SelectField('Plano', choices=[], validate_choice=False, coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        """    Função que válida as informações do formulário    """
        check_validate = super(TelaPlanoForm, self).validate()  # válida inicialmente as informações

        if check_validate:
            viewplan = Telaplano.query.filter_by(plano_id=self.plano.data, tela_id=self.tela.data).one_or_none()
            if viewplan:
                flash("Tela já registrada para este plano", category="danger")
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
