import datetime

from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, SubmitField, SelectField, FileField, \
    DecimalField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional, NumberRange
from flask import flash
from flask_login import current_user


class PlanoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do plano de manutenção"})
    codigo = StringField('Código', validators=[Optional(), Length(max=50)],
                         render_kw={"placeholder": "Digite o código do plano de manutenção"})
    cod_automatico = BooleanField('Gerar Código Automáticamente?')
    data_inicio = DateField('Data de Início', validators=[InputRequired()],
                            render_kw={"placeholder": "Digite a data de início"})
    tipoordem = SelectField('Tipo de Ordem Serviço', choices=[], coerce=int, validators=[InputRequired()])
    tipodata = SelectField('Tipo de data inicial', choices=[], coerce=int, validators=[InputRequired()])
    cancelamento_data = BooleanField('Cancelar automaticamente?')
    periodicidade = SelectField('Periodicidade', choices=[], coerce=int, validators=[InputRequired()])
    equipamento = SelectField('Equipamento', choices=[], coerce=int, validators=[InputRequired()])

    total_tecnico = IntegerField('Total de Técnicos', validators=[InputRequired(), NumberRange(min=1, max=100)],
                                 render_kw={"placeholder": "Digite o total de técnico "})
    tempo_estimado = DecimalField('Tempo estimado (h)', places=2, rounding=None,
                                  validators=[InputRequired()],
                                  render_kw={"placeholder": "Digite o tempo estimado "})

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
            elif self.tipodata.data == 0:
                flash("Tipo de Data Inicial não informada", category="danger")
                return False
            elif self.tipoordem.data == 0:
                flash("Tipo de Ordem de Serviço não informado", category="danger")
                return False
            else:
                return True

        return False


class AtividadeForm(Form):
    posicao = IntegerField('Posição', validators=[InputRequired(), NumberRange(min=1, max=100)],
                           render_kw={"placeholder": "Posição "})
    descricao = StringField('Descrição', validators=[InputRequired(), Length(max=100)],
                            render_kw={"placeholder": "Atividade"})
    listaatividade_id = IntegerField()
    tipoparametro_id = SelectField('Valor:', choices=[], coerce=int, validate_choice=False)
    valorbinario_id = SelectField('Valor:', choices=[], coerce=int, validate_choice=False)
    valorinteiro = IntegerField('Valor:')
    valordecimal = DecimalField('Valor', places=2, rounding=None)
    valortexto = TextAreaField('Valor:', validators=[Optional(), Length(max=100)])

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        check_validate = super(AtividadeForm, self).validate()

        if check_validate:
            return True

        return False


class ListaAtividadeForm(Form):
    observacao = TextAreaField('Observação:', validators=[InputRequired(), Length(min=10, max=300)])

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        check_validate = super(ListaAtividadeForm, self).validate()

        if check_validate:
            return True

        return False
