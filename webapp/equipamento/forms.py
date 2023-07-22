from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, \
    SubmitField, SelectField, FileField, DecimalField
from wtforms.validators import InputRequired, Length, Optional
from flask import flash


class GrupoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do grupo"})
    ativo = BooleanField('Ativo', render_kw={"placeholder": "Informe se o grupo está ativo"})
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de grupos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(GrupoForm, self).validate()
        if check_validate:
            if self.nome.data == '':
                flash("Nome do grupo não foi informado", category="danger")
                return False
            else:
                return True

        return False


class SubgrupoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do sistema"})
    ativo = BooleanField('Ativo', render_kw={"placeholder": "Informe se o sistema está ativo"})
    grupo = SelectField('Grupo de equipamentos', choices=[], coerce=int)
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de subgrupos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):
        check_validate = super(SubgrupoForm, self).validate()

        if check_validate:
            if self.grupo.data == 0:
                flash("Grupo não foi informado", category="danger")
                return False
            else:
                return True

        return False


class EquipamentoForm(Form):
    cod = StringField('Código', validators=[InputRequired(), Length(max=50)],
                      render_kw={"placeholder": "Digite o código"})
    descricao_curta = StringField('Descrição Curta', validators=[InputRequired()],
                                  render_kw={"placeholder": "Digite a descrição curta"})
    descricao_longa = StringField('Descrição Longa', render_kw={"placeholder": "Digite a descrição longa"})
    fabricante = StringField('Fabrica', validators=[Optional()],
                             render_kw={"placeholder": "Digite o nome da Fabrica"})
    marca = StringField('Marca', validators=[Optional()],
                        render_kw={"placeholder": "Digite marca"})
    modelo = StringField('Modelo', validators=[Optional()],
                         render_kw={"placeholder": "Digite o modelo "})
    ns = StringField('Número de Série', validators=[Optional()],
                     render_kw={"placeholder": "Digite o número de série"})
    largura = IntegerField('Largura (mm)', validators=[Optional()],
                           render_kw={"placeholder": "Digite a largura "})
    comprimento = IntegerField('Comprimento (mm)', validators=[Optional()],
                               render_kw={"placeholder": "Digite o comprimento"})
    altura = IntegerField('Altura (mm)', validators=[Optional()],
                          render_kw={"placeholder": "Digite a altura"})
    peso = IntegerField('Peso (kg)', validators=[Optional()],
                        render_kw={"placeholder": "Digite o peso"})
    potencia = IntegerField('Potencia (kw)', validators=[Optional()], render_kw={"placeholder": "Digite a potência"})
    tensao = IntegerField('Tensão (V)', validators=[Optional()], render_kw={"placeholder": "Digite a tensão"})
    data_fabricacao = DateField('Ano de Fabricação', validators=[Optional()],
                                render_kw={"placeholder": "Digite o ano de fabricação"})
    data_aquisicao = DateField('Data de Aquisição', validators=[Optional()],
                               render_kw={"placeholder": "Digite a data da aquisição"})
    data_instalacao = DateField('Data da Instalação', validators=[Optional()],
                                render_kw={"placeholder": "Digite a data da instalação"})
    custo_aquisicao = DecimalField('Custo de Aquisição (R$)', places=2, rounding=None, validators=[Optional()],
                                   render_kw={"placeholder": "Digite o custo de aquisição"})
    depreciacao = IntegerField('Depreciação (Anos)', validators=[Optional()],
                               render_kw={"placeholder": "Digite o tempo de depreciação"})
    tag = StringField('Tag ', validators=[InputRequired()], render_kw={"placeholder": "Digite a tag"})
    patrimonio = StringField('Patrimonio', validators=[Optional()],
                             render_kw={"placeholder": "Digite o patrimônio"})
    localizacao = StringField('Localizacao', validators=[Optional()],
                              render_kw={"placeholder": "Digite a localização"})
    latitude = StringField('Latitude', validators=[Optional()],
                           render_kw={"placeholder": "Digite a latitude"})
    longitude = StringField('longitude', validators=[Optional()],
                            render_kw={"placeholder": "Digite a longitude"})

    centro_custo = StringField('Centro de Custo', validators=[Optional()],
                               render_kw={"placeholder": "Digite o centro de custo"})
    ativo = BooleanField('Ativo ', render_kw={"placeholder": "Digite se está ativo"})
    subgrupo = SelectField('Subgrupo de equipamentos', choices=[], coerce=int)

    # title = StringField('Nome do arquivo',  validators=[Optional(), Length(50)])
    file = FileField('Escolha um arquivo para o cadastro de equipamentos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        check_validate = super(EquipamentoForm, self).validate()

        if check_validate:
            if self.subgrupo.data == 0:
                flash("Subgrupo não informado", category="danger")
                return False
            else:
                return True
        return False
