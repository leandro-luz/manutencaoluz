from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import current_user, login_required
from .models import db, Asset, Group, System
from webapp.company.models import Company
from .forms import AssetForm, GroupForm, SystemForm

asset_blueprint = Blueprint(
    'asset',
    __name__,
    template_folder='../templates/sistema/asset',
    url_prefix="/system"
)


@asset_blueprint.route('/asset_list', methods=['GET', 'POST'])
@login_required
def asset_list():
    assets = Asset.query.filter_by(company_id=current_user.company_id).all()
    return render_template('asset_list.html', assets=assets)


@asset_blueprint.route('/asset_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def asset_edit(id):
    if id > 0:
        # Atualizar
        asset = Asset.query.filter_by(id=id).first()
        form = AssetForm(obj=asset)

        # Atualizar ou Ler dados
        if form.company.data:
            c_d = form.company.data
            g_d = form.group.data
        else:
            c_d = asset.company_id
            g_d = asset.group_id

    else:
        # Cadastrar
        asset = Asset()
        asset.id = 0
        form = AssetForm()
        c_d = form.company.data
        g_d = form.group.data

    # Listas

    form.company.choices = [(companies.id, companies.name) for companies
                            in Company.query.filter_by(id=current_user.company_id).all()]
    ##perfil superadmin
    # form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]
    form.company.data = c_d

    form.group.choices = [(groups.id, groups.name) for groups
                          in Group.query.filter_by(company_id=current_user.company_id)]
    form.group.data = g_d

    form.system.choices = [(systems.id, systems.name) for systems in System.query.filter_by(asset_id=asset.id).all()]

    # Validação
    if form.validate_on_submit():
        asset.change_attributes(form)
        db.session.add(asset)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Equipamento atualizado", category="success")
        else:
            flash("Equipamento cadastrado", category="success")

        return redirect(url_for("asset.asset_list"))
    return render_template("asset_edit.html", form=form, asset=asset)


@asset_blueprint.route('/asset_active/<int:id>', methods=['GET', 'POST'])
@login_required
def asset_active(id):
    asset_ = Asset.query.filter_by(id=id).one()
    if asset_:
        asset_.change_active()
        db.session.add(asset_)
        db.session.commit()
    return redirect(url_for('asset.asset_list'))


@asset_blueprint.route('/group_list', methods=['GET', 'POST'])
@login_required
def group_list():
    groups = Group.query.filter_by(company_id=current_user.company_id).all()
    return render_template('group_list.html', groups=groups)


@asset_blueprint.route('/group_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def group_edit(id):
    if id > 0:
        # Atualizar
        group = Group.query.filter_by(id=id).first()
        form = GroupForm(obj=group)

        # Atualizar ou Ler dados
        if form.company.data:
            c_d = form.company.data
        else:
            c_d = group.company_id

    else:
        # Cadastrar
        group = Group()
        group.id = 0
        form = GroupForm()
        c_d = form.company.data

    # Listas
    form.company.choices = [(companies.id, companies.name) for companies
                            in Company.query.filter_by(id=current_user.company_id).all()]
    ##perfil superadmin
    # form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]
    form.company.data = c_d

    # Validação
    if form.validate_on_submit():
        group.change_attributes(form)
        db.session.add(group)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Grupo atualizado", category="success")
        else:
            flash("Grupo cadastrado", category="success")

        return redirect(url_for("asset.group_list"))
    return render_template("group_edit.html", form=form, group=group)


@asset_blueprint.route('/system_list/<int:id>', methods=['GET', 'POST'])
@login_required
def system_list(id):
    systems = System.query.filter_by(asset_id=id).all()
    return render_template('system_list.html', systems=systems, id=id)


@asset_blueprint.route('/system_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def system_edit(id):
    if id > 0:
        # Atualizar
        system = System.query.filter_by(id=id).first()
        form = SystemForm(obj=system)

        # Atualizar ou Ler dados
        if form.asset.data:
            a_d = form.asset.data
        else:
            a_d = system.asset_id

    else:
        # Cadastrar
        system = System()
        system.id = 0
        form = SystemForm()
        a_d = form.asset.data
        id = form.asset.data

    # Listas
    form.asset.choices = [(assets.id, assets.short_description) for assets in Asset.query.all()]
    form.asset.data = a_d

    # Validação
    if form.validate_on_submit():
        system.change_attributes(form)
        db.session.add(system)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Sistema atualizado", category="success")
        else:
            flash("Sistema cadastrado", category="success")

        return redirect(url_for("asset.system_list", id=id))
    return render_template("system_edit.html", form=form, system=system, id=id)
