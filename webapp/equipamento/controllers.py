from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from .models import Equipamento, Grupo, Sistema
from .forms import EquipamentoForm, GrupoForm, SistemaForm
from webapp.usuario import has_view
from webapp.utils.files import file_standard

empresa_blueprint = Blueprint(
    'equipamento',
    __name__,
    template_folder='../templates/sistema/equipamento',
    url_prefix="/sistema"
)


@empresa_blueprint.route('/asset_list', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def asset_list():
    """Retorna a lista de equipamentos"""
    equipamentos = Equipamento.query.filter_by(empresa_id=current_user.empresa_id).all()
    return render_template('asset_list.html', equipamentos=equipamentos)


@empresa_blueprint.route('/asset_edit/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def asset_edit(equipamento_id):
    if equipamento_id > 0:
        # Atualizar
        equipamento = Equipamento.query.filter_by(id=equipamento_id).first()

        if equipamento:
            form = EquipamentoForm(obj=equipamento)

            # Atualizar ou Ler dados
            if form.grupo.data:
                g_d = form.grupo.data
            else:
                g_d = equipamento.grupo_id
        else:
            flash("Equipamento não localizado", category="danger")
            return redirect(url_for("equipamento.asset_list"))
    else:
        # Cadastrar
        equipamento = Equipamento()
        equipamento.id = 0
        form = EquipamentoForm()
        g_d = form.grupo.data

    # Listas
    form.grupo.choices = [(groups.id, groups.nome) for groups in
                          Grupo.query.filter_by(empresa_id=current_user.empresa_id, ativo=True).all()]
    form.grupo.data = g_d

    form.sistema.choices = [(systems.id, systems.nome) for systems in
                            Sistema.query.filter_by(equipamento_id=equipamento.id, ativo=True).all()]

    # Validação
    if form.validate_on_submit():
        equipamento.alterar_atributos(form)
        if equipamento.salvar():
            # Mensagens
            if equipamento_id > 0:
                flash("Equipamento atualizado", category="success")
            else:
                flash("Equipamento cadastrado", category="success")

        return redirect(url_for("equipamento.asset_list"))
    return render_template("asset_edit.html", form=form, equipamento=equipamento)


@empresa_blueprint.route('/asset_active/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def asset_active(equipamento_id):
    equipamento = Equipamento.query.filter_by(id=equipamento_id).one_or_none()
    if equipamento:
        equipamento.ativar_desativar()
        equipamento.salvar()

    else:
        flash("Equipamento não localizado", category="danger")
    return redirect(url_for('equipamento.asset_list'))


@empresa_blueprint.route('/asset_file_out/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def asset_file_out():
    result, path = file_standard(file_name=Equipamento.nome_doc, titles=Equipamento.titulos_doc)
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
        return redirect(url_for("equipamento.asset_list"))
    else:
        flash("Não foi gerado o arquivo padrão", category="dander")
        return redirect(url_for("equipamento.asset_list"))


@empresa_blueprint.route('/asset_file_int/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def asset_file_int():
    print('entrada da lista para o cadastro de equipamentos em lote')

    # file = request.files['file']
    # print(file.razao_social)
    # print(file.headers)

    return redirect(url_for("equipamento.asset_list"))


@empresa_blueprint.route('/group_list/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def group_list(equipamento_id):
    grupos = Grupo.query.filter_by(empresa_id=current_user.empresa_id).filter(Grupo.nome.notlike("%None%")).all()
    return render_template('group_list.html', grupos=grupos, equipamento_id=equipamento_id)


@empresa_blueprint.route('/group_edit/<int:grupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def group_edit(grupo_id, equipamento_id):
    if grupo_id > 0:
        # Atualizar
        grupo = Grupo.query.filter_by(id=grupo_id).first()

        if grupo:
            form = GrupoForm(obj=grupo)
        else:
            flash("Grupo não localizado", category="danger")
            return redirect(url_for("equipamento.group_list", equipamento_id=equipamento_id))

    else:
        # Cadastrar
        grupo = Grupo()
        grupo.id = 0
        form = GrupoForm()

    # Validação
    if form.validate_on_submit():
        grupo.alterar_atributos(form)
        grupo.salvar()

        # Mensagens
        if grupo_id > 0:
            flash("Grupo atualizado", category="success")
        else:
            flash("Grupo cadastrado", category="success")

        return redirect(url_for("equipamento.group_list", equipamento_id=equipamento_id))
    return render_template("group_edit.html", form=form, grupo=grupo, equipamento_id=equipamento_id)


@empresa_blueprint.route('/system_list/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def system_list(equipamento_id):
    sistemas = Sistema.query.filter_by(equipamento_id=equipamento_id).all()
    return render_template('system_list.html', sistemas=sistemas, equipamento_id=equipamento_id)


@empresa_blueprint.route('/system_edit/<int:sistema_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def system_edit(sistema_id, equipamento_id):
    if sistema_id > 0:
        # Atualizar
        sistema = Sistema.query.filter_by(id=sistema_id).first()

        if sistema:
            form = SistemaForm(obj=sistema)
        else:
            flash("Sistema não localizado", category="danger")
            return redirect(url_for("equipamento.system_list", equipamento_id=equipamento_id))

    else:
        # Cadastrar
        sistema = Sistema()
        sistema.id = 0
        form = SistemaForm()

    # Validação
    if form.validate_on_submit():
        sistema.alterar_atributos(form)
        sistema.equipamento_id=equipamento_id
        sistema.salvar()

        # Mensagens
        if sistema_id > 0:
            flash("Sistema atualizado", category="success")
        else:
            flash("Sistema cadastrado", category="success")

        return redirect(url_for("equipamento.system_list", equipamento_id=equipamento_id))

    return render_template("system_edit.html", form=form, sistema=sistema, sistema_id=sistema_id, equipamento_id=equipamento_id)
