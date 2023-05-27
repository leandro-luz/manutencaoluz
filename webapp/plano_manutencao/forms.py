from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Optional



class PlanoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do plano de manutenção"})
    codigo = StringField('Código', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o código do plano de manutenção"})

    tipodata = SelectField('Tipo de data inicial', choices=[], coerce=int)
    periodicidade = SelectField('Periodicidade', choices=[], coerce=int)
    equipamento = SelectField('Equipamento', choices=[], coerce=int)
    file = FileField('Escolha um arquivo para o cadastro de planos de manutenção em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    ativo = BooleanField('Ativo', render_kw={"placeholder": "Informe se o plano está ativo"})
    submit = SubmitField("Salvar")

    def validate(self, **kwargs):

        check_validate = super(PlanoForm, self).validate()

        if check_validate:
            return True

        return False
