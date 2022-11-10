from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from .models import Asset
from flask import flash


class AssetForm(Form):
    cod = StringField('Código', validators=[DataRequired(), Length(max=50)],
                      render_kw={"placeholder": "Digite o código"})
    short_description = StringField('Descrição Curta', validators=[DataRequired()],
                                    render_kw={"placeholder": "Digite a descrição curta"})
    long_description = StringField('Descrição Longa', render_kw={"placeholder": "Digite a descrição longa"})
    manufacturer = StringField('Fabrica', render_kw={"placeholder": "Digite o nome da Fabrica"})
    brand = StringField('Marca',
                        render_kw={"placeholder": "Digite marca"})
    model = StringField('Modelo ',
                        render_kw={"placeholder": "Digite o modelo "})
    ns = StringField('Número de Série ',
                     render_kw={"placeholder": "Digite o número de série"})
    dimension_x = IntegerField('Largura ',
                               render_kw={"placeholder": "Digite a largura "})
    dimension_y = IntegerField('Comprimento ',
                               render_kw={"placeholder": "Digite o comprimento"})
    dimension_z = IntegerField('Altura ',
                               render_kw={"placeholder": "Digite a altura"})
    weight = IntegerField('Peso ',
                          render_kw={"placeholder": "Digite o peso"})
    year_manufacture = DateField('Ano de Fabridcação ',
                                    render_kw={"placeholder": "Digite o ano de fabricação"})
    date_acquisition = DateField('Data de Aquisição ',
                                 render_kw={"placeholder": "Digite a data da aquisição"})
    date_installation = DateField('Data da Instalação ',
                                  render_kw={"placeholder": "Digite a data da instalação"})
    cost_acquisition = IntegerField('Custo de Aquisição ',
                                    render_kw={"placeholder": "Digite o custo de aquisição"})
    depreciation = IntegerField('Depreciação ',
                                render_kw={"placeholder": "Digite o tempo de depreciação"})
    tag = IntegerField('Tag ',
                       render_kw={"placeholder": "Digite a tag"})
    cost_center = StringField('Centro de Custo ',
                              render_kw={"placeholder": "Digite o centro de custo"})
    active = BooleanField('Ativo ',
                          render_kw={"placeholder": "Digite se está ativo"})
    type_id = IntegerField('Grupo',
                           render_kw={"placeholder": "Digite o grupo de ativos"})
    company = SelectField('Empresa', choices=[])
    submit = SubmitField("Salvar")

    def validate(self):
        # # if our validators do not pass
        # check_validate = super(AssetForm, self).validate()
        # if not check_validate:
        #     print('False')
        #     return False
        return True
