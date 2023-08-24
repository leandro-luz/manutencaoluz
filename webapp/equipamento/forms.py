from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, \
    SubmitField, SelectField, FileField, DecimalField
from wtforms.validators import InputRequired, Length, Optional
from webapp.equipamento.models import *
from flask import flash


class GrupoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do grupo"})
    ativo = BooleanField('Ativo', render_kw={"placeholder": "Informe se o grupo está ativo"})
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de grupos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):

        check_validate = super(GrupoForm, self).validate()
        if check_validate:
            if self.nome.data == '':
                flash("Nome do grupo não foi informado", category="danger")
                return False
            if Grupo.query.filter(
                    Grupo.nome == self.nome.data,
                    Grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um grupo com este nome", category="danger")
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
            if Subgrupo.query.filter(
                    Subgrupo.nome == self.nome.data,
                    Subgrupo.grupo_id == self.grupo.data,
                    Grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um subgrupo com este nome para este grupo", category="danger")
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

    latitude = StringField('Latitude', validators=[Optional()],
                           render_kw={"placeholder": "Digite a latitude"})
    longitude = StringField('longitude', validators=[Optional()],
                            render_kw={"placeholder": "Digite a longitude"})

    centro_custo = StringField('Centro de Custo', validators=[Optional()],
                               render_kw={"placeholder": "Digite o centro de custo"})
    ativo = BooleanField('Ativo ', render_kw={"placeholder": "Digite se está ativo"})

    localizacao = SelectField('Localização', choices=[], coerce=int)
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

            if Equipamento.query.filter(
                    Equipamento.cod == self.cod.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este código", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.descricao_curta == self.descricao_curta.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este descrição curta", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.descricao_longa == self.descricao_longa.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este descrição longa", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.ns == self.ns.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este número de série", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.tag == self.tag.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com esta tag", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.patrimonio == self.patrimonio.data,
                    Equipamento.subgrupo.grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este patrimônio", category="danger")
                return False

            else:
                return True
        return False


class LocalizacaoForm(Form):
    nome = StringField('Nome')
    setor = SelectField('Setor', choices=[], coerce=int)
    local = SelectField('Local', choices=[], coerce=int)
    pavimento = SelectField('Pavimento', choices=[], coerce=int)
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de pavimentos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):

        # # if our validators do not pass
        check_validate = super(LocalizacaoForm, self).validate()
        if check_validate:
            if self.setor.data == 0:
                flash("O setor não foi selecionado", category="danger")
                return False
            elif self.local.data == 0:
                flash("O local não foi selecionado", category="danger")
                return False
            elif self.pavimento.data == 0:
                flash("O pavimento não foi selecionado", category="danger")
                return False

            if Localizacao.query.filter(
                    Localizacao.nome == self.nome.data,
                    Local.id == Localizacao.local_id,
                    Setor.id == Local.setor_id,
                    Setor.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe uma localização com este nome", category="danger")
                return False
            else:
                return True

        return False


class PavimentoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do pavimento"})
    sigla = StringField('Sigla', validators=[InputRequired(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla do pavimento"})
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de pavimentos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(PavimentoForm, self).validate()
        if check_validate:
            if self.nome.data == '':
                flash("Nome do pavimento não foi informado", category="danger")
                return False
            elif self.sigla.data == '':
                flash("Sigla do pavimento não foi informada", category="danger")
                return False
            elif Pavimento.query.filter(
                    Pavimento.nome == self.nome.data,
                    Pavimento.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um pavimento com este nome", category="danger")
                return False
            elif Pavimento.query.filter(
                    Pavimento.sigla == self.sigla.data,
                    Pavimento.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um pavimento com esta sigla", category="danger")
                return False
            else:
                return True

        return False


class LocalForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do local"})
    sigla = StringField('Sigla', validators=[InputRequired(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla do local"})

    setor = SelectField('Setor', choices=[], coerce=int)

    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de locais em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(LocalForm, self).validate()
        if check_validate:
            if self.nome.data == '':
                flash("Nome do local não foi informado", category="danger")
                return False
            elif self.sigla.data == '':
                flash("Sigla do local não foi informada", category="danger")
                return False
            elif self.setor.data == 0:
                flash("Setor não foi selecionado", category="danger")
                return False
            if Local.query.filter(
                    Local.nome == self.nome.data,
                    Setor.id == self.setor.data,
                    Setor.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um local com este nome para este setor", category="danger")
                return False
            if Local.query.filter(
                    Local.sigla == self.sigla.data,
                    Setor.id == self.setor.data,
                    Setor.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe este um local com esta sigla", category="danger")
                return False
            else:
                return True
        return False


class SetorForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do setor"})
    sigla = StringField('Sigla', validators=[InputRequired(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla do setor"})

    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de setores em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(SetorForm, self).validate()
        if check_validate:
            if self.nome.data == '':
                flash("Nome do sertor não foi informado", category="danger")
                return False
            elif self.sigla.data == '':
                flash("Sigla do setor não foi informada", category="danger")
                return False
            elif Setor.query.filter(
                    Setor.nome == self.nome.data,
                    Setor.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um setor com este nome", category="danger")
                return False
            elif Setor.query.filter(
                    Setor.sigla == self.sigla.data,
                    Setor.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um setor com esta sigla", category="danger")
                return False
            else:
                return True
        return False
