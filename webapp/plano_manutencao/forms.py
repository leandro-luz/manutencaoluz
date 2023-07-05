from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Optional
from flask import flash


class PlanoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do plano de manutenção"})
    codigo = StringField('Código', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o código do plano de manutenção"})
    data_inicio = DateField('Data de Início', validators=[InputRequired()],
                               render_kw={"placeholder": "Digite a data de início"})
    tipoordem = SelectField('Tipo de Ordem Serviço', choices=[], coerce=int, validators=[InputRequired()])
    tipodata = SelectField('Tipo de data inicial', choices=[], coerce=int, validators=[InputRequired()])
    periodicidade = SelectField('Periodicidade', choices=[], coerce=int, validators=[InputRequired()])
    equipamento = SelectField('Equipamento', choices=[], coerce=int, validators=[InputRequired()])
    file = FileField('Escolha um arquivo para o cadastro de planos de manutenção em Lote (4MB):',
                     validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    ativo = BooleanField('Ativo', render_kw={"placeholder": "Informe se o plano está ativo"})
    submit = SubmitField("Salvar")

    def validate(self, **kwargs):

        check_validate = super(PlanoForm, self).validate()

        if check_validate:
            if self.equipamento.data == 0:
                flash("Equipamento não informado", category="danger")
                return False
            elif self.periodicidade.data == 0:
                flash("Periodicidade não informada", category="danger")
                return False
            elif self.tipoordem.data == 0:
                flash("Tipo de Ordem de Serviço não informado", category="danger")
                return False
            else:
                return True

        return False
