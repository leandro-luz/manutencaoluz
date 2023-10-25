from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, DateField, BooleanField, \
    SubmitField, SelectField, FileField, DecimalField
from wtforms.validators import InputRequired, Length, Optional
from webapp.equipamento.models import *
from flask import flash
from flask_login import current_user


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
                    current_user.empresa_id == Grupo.empresa_id,
                    Grupo.nome == self.nome.data,
            ).one_or_none():
                flash("Já existe um grupo com este nome", category="danger")
                return False
            else:
                return True

        return False


class SubgrupoForm(Form):
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do sistema"})
    submit = SubmitField("Salvar")

    file = FileField('Escolha um arquivo para o cadastro de subgrupos em Lote (4MB):', validators=[Optional()],
                     render_kw={"placeholder": "Selecione o arquivo"})

    def validate(self, **kwargs):

        check_validate = super(SubgrupoForm, self).validate()

        if check_validate:
            if self.nome.data == '':
                flash("Nome do subgrupo não foi informado", category="danger")
                return False
            if Subgrupo.query.filter(
                    current_user.empresa_id == Grupo.empresa_id,
                    Grupo.id == Subgrupo.grupo_id,
                    Subgrupo.nome == self.nome.data,
            ).one_or_none():
                flash("Já existe um subgrupo com este nome", category="danger")
                return False
            else:
                return True

        return False


class EquipamentoForm(Form):
    id = IntegerField('Id')
    cod = StringField('Código', validators=[Optional(), Length(max=50)],
                      render_kw={"placeholder": "Digite o código"})
    cod_automatico = BooleanField('Gerar Código Automáticamente?')

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
    tag = StringField('Tag ', validators=[Optional()], render_kw={"placeholder": "Digite a tag"})
    tag_automatico = BooleanField('Gerar Tag Automáticamente?')

    patrimonio = StringField('Patrimonio', validators=[Optional()],
                             render_kw={"placeholder": "Digite o patrimônio"})

    latitude = StringField('Latitude', validators=[Optional()],
                           render_kw={"placeholder": "Digite a latitude"})
    longitude = StringField('longitude', validators=[Optional()],
                            render_kw={"placeholder": "Digite a longitude"})

    centro_custo = StringField('Centro de Custo', validators=[Optional()],
                               render_kw={"placeholder": "Digite o centro de custo"})
    ativo = BooleanField('Ativo ', render_kw={"placeholder": "Digite se está ativo"})

    setor = SelectField('Setor', choices=[], coerce=int)
    local = SelectField('Local', choices=[], coerce=int)
    pavimento = SelectField('Pavimento', choices=[], coerce=int)

    vazao_valor = DecimalField('Vazão', places=2, rounding=None, validators=[Optional()],
                               render_kw={"placeholder": "Digite a vazão"})
    volume_valor = DecimalField('Volume', places=2, rounding=None, validators=[Optional()],
                                render_kw={"placeholder": "Digite o volume"})
    area_valor = DecimalField('Área', places=2, rounding=None, validators=[Optional()],
                              render_kw={"placeholder": "Digite a área"})
    largura_valor = DecimalField('Largura', places=2, rounding=None, validators=[Optional()],
                                 render_kw={"placeholder": "Digite a largura "})
    comprimento_valor = DecimalField('Comprimento', places=2, rounding=None, validators=[Optional()],
                                     render_kw={"placeholder": "Digite o comprimento"})
    altura_valor = DecimalField('Altura', places=2, rounding=None, validators=[Optional()],
                                render_kw={"placeholder": "Digite a altura"})
    peso_valor = DecimalField('Peso', places=2, rounding=None, validators=[Optional()],
                              render_kw={"placeholder": "Digite o peso"})
    potencia_valor = DecimalField('Potencia', places=2, rounding=None, validators=[Optional()],
                                  render_kw={"placeholder": "Digite a potência elétrica"})
    tensao_valor = DecimalField('Tensão', places=2, rounding=None, validators=[Optional()],
                                render_kw={"placeholder": "Digite a tensão elétrica"})

    und_vazao = SelectField('unidade', choices=[], coerce=int)
    und_volume = SelectField('unidade', choices=[], coerce=int)
    und_area = SelectField('unidade', choices=[], coerce=int)
    und_altura = SelectField('unidade', choices=[], coerce=int)
    und_largura = SelectField('unidade', choices=[], coerce=int)
    und_comprimento = SelectField('unidade', choices=[], coerce=int)
    und_peso = SelectField('unidade', choices=[], coerce=int)
    und_potencia = SelectField('unidade', choices=[], coerce=int)
    und_tensao = SelectField('unidade', choices=[], coerce=int)

    grupo = SelectField('Grupo', choices=[], coerce=int)
    subgrupo = SelectField('Subgrupo', choices=[], coerce=int)

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
                    Equipamento.id != self.id.data,
                    Equipamento.cod == self.cod.data,
                    Equipamento.subgrupo_id == Subgrupo.id,
                    Subgrupo.grupo_id == Grupo.id,
                    Grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este código", category="danger")
                return False

            if Equipamento.query.filter(
                    Equipamento.id != self.id.data,
                    Equipamento.descricao_curta == self.descricao_curta.data,
                    Equipamento.subgrupo_id == Subgrupo.id,
                    Subgrupo.grupo_id == Grupo.id,
                    Grupo.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe equipamento com este descrição curta", category="danger")
                return False

            if self.descricao_longa.data:
                if Equipamento.query.filter(
                        Equipamento.id != self.id.data,
                        Equipamento.descricao_longa == self.descricao_longa.data,
                        Equipamento.subgrupo_id == Subgrupo.id,
                        Subgrupo.grupo_id == Grupo.id,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe equipamento com este descrição longa", category="danger")
                    return False

            if self.ns.data:
                if Equipamento.query.filter(
                        Equipamento.id != self.id.data,
                        Equipamento.ns == self.ns.data,
                        Equipamento.subgrupo_id == Subgrupo.id,
                        Subgrupo.grupo_id == Grupo.id,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe equipamento com este número de série", category="danger")
                    return False

            if self.tag.data:
                if Equipamento.query.filter(
                        Equipamento.id != self.id.data,
                        Equipamento.tag == self.tag.data,
                        Equipamento.subgrupo_id == Subgrupo.id,
                        Subgrupo.grupo_id == Grupo.id,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe equipamento com esta tag", category="danger")
                    return False

            if self.patrimonio.data:
                if Equipamento.query.filter(
                        Equipamento.id != self.id.data,
                        Equipamento.patrimonio == self.patrimonio.data,
                        Equipamento.subgrupo_id == Subgrupo.id,
                        Subgrupo.grupo_id == Grupo.id,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe equipamento com este patrimônio", category="danger")
                    return False

            else:
                return True
        return False


class LocalizacaoForm(Form):
    id = IntegerField('id')
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome"})
    sigla = StringField('Sigla', validators=[InputRequired(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla"})
    tipo = SelectField('Tipo', choices=[], coerce=int, validate_choice=False, )

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(LocalizacaoForm, self).validate()

        if check_validate:

            if self.tipo.data == 0:
                flash("Tipo de localização não selecionado", category="danger")
                return False

            # Se o tipo selecionador por Setor
            if self.tipo.data == 1:
                if Setor.query.filter(
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

            # Se o tipo selecionador por Local
            if self.tipo.data == 2:
                if Local.query.filter(
                        Local.nome == self.nome.data,
                        Local.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe um local com este nome para este setor", category="danger")
                    return False

                if Local.query.filter(
                        Local.sigla == self.sigla.data,
                        Local.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe este um local com esta sigla", category="danger")
                    return False

            # Se o tipo selecionador por Pavimento
            if self.tipo.data == 3:
                if Pavimento.query.filter(
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

            return True

        return False


class AgrupamentoForm(Form):
    id = IntegerField('id')
    nome = StringField('Nome', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome"})
    tipo = SelectField('Tipo', choices=[], coerce=int, validate_choice=False, )
    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(AgrupamentoForm, self).validate()

        if check_validate:
            if self.tipo.data == 0:
                flash("Tipo de agrupamento não selecionado", category="danger")
                return False

            # Se o tipo selecionador por Grupo
            if self.tipo.data == 1:
                if Grupo.query.filter(
                        Grupo.nome == self.nome.data,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe um grupo com este nome", category="danger")
                    return False

            # Se o tipo selecionador por Subgrupo
            if self.tipo.data == 2:
                if Subgrupo.query.filter(
                        Subgrupo.nome == self.nome.data,
                        Subgrupo.grupo_id == Grupo.id,
                        Grupo.empresa_id == current_user.empresa_id
                ).one_or_none():
                    flash("Já existe um subgrupo com este nome para este grupo", category="danger")
                    return False

            return True
        else:
            return False


class SetorForm(Form):
    id = IntegerField('id')
    nome = StringField('Nome', validators=[Optional(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome"})
    sigla = StringField('Sigla', validators=[Optional(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla"})

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(SetorForm, self).validate()

        if check_validate:
            if Setor.query.filter(
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
            if not self.nome.data and not self.sigla.data:
                flash("Não foi preenchido nenhum valor para alterar", category="danger")
                return False
            return True
        return False


class LocalForm(Form):
    id = IntegerField('id')
    nome = StringField('Nome', validators=[Optional(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome"})
    sigla = StringField('Sigla', validators=[Optional(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla"})

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(LocalForm, self).validate()

        if check_validate:
            if Local.query.filter(
                    Local.nome == self.nome.data,
                    Local.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe um local com este nome para este setor", category="danger")
                return False

            if Local.query.filter(
                    Local.sigla == self.sigla.data,
                    Local.empresa_id == current_user.empresa_id
            ).one_or_none():
                flash("Já existe este um local com esta sigla", category="danger")
                return False
            if not self.nome.data and not self.sigla.data:
                flash("Não foi preenchido nenhum valor para alterar", category="danger")
                return False
            return True
        return False


class PavimentoForm(Form):
    id = IntegerField('id')
    nome = StringField('Nome', validators=[Optional(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome"})
    sigla = StringField('Sigla', validators=[Optional(), Length(max=5)],
                        render_kw={"placeholder": "Digite a sigla"})

    submit = SubmitField("Salvar")

    def validate(self, **kwargs):
        # # if our validators do not pass
        check_validate = super(PavimentoForm, self).validate()

        if check_validate:
            if Pavimento.query.filter(
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
            if not self.nome.data and not self.sigla.data:
                flash("Não foi preenchido nenhum valor para alterar", category="danger")
                return False
            return True
        return False
