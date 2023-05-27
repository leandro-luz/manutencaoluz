from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Optional



class OrdemServicoForm(Form):
    descricao = StringField('Descrição', validators=[InputRequired(), Length(max=50)],
                         render_kw={"placeholder": "Descrição da atividade"})
    equipamento = SelectField('Equipamento', choices=[], coerce=int)
    situacaoordem = SelectField('Situação', choices=[], coerce=int, validate_choice=False)

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):

        check_validate = super(OrdemServicoForm, self).validate()

        if check_validate:
            return True

        return False