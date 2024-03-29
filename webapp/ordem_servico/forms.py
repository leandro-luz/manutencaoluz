from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, TextAreaField, SubmitField, SelectField, \
    FileField
from wtforms.validators import InputRequired, Length, Optional
from flask import flash
from flask_login import current_user


class OrdemServicoForm(Form):
    descricao = StringField('Descrição', validators=[InputRequired(), Length(max=50)],
                            render_kw={"placeholder": "Descrição da atividade"})
    tipo = SelectField('Tipo de Ordem', choices=[], coerce=int)
    equipamento = SelectField('Equipamento', choices=[], coerce=int)

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):

        check_validate = super(OrdemServicoForm, self).validate()

        if check_validate:
            if self.equipamento.data == 0:
                flash("Equipamento não informado", category="danger")
                return False
            elif self.tipo.data == 0:
                flash("Tipo de Ordem não informado", category="danger")
                return False
            else:
                return True

        return False


class TramitacaoForm(Form):
    observacao = TextAreaField('Observação', validators=[InputRequired()],
                               render_kw={"placeholder": "Informe a observação"})
    tiposituacaoordem = SelectField('Situação', choices=[], coerce=int, validate_choice=False)
    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        check_validate = super(TramitacaoForm, self).validate()
        if check_validate:
            if self.tiposituacaoordem.data == 0:
                flash("Tipo da situação não informada", category="danger")
                return False
            else:
                return True

        return False
