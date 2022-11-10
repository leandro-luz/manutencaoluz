from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import login_user, logout_user, current_user, login_required
from .models import db, Asset
from webapp.company.models import Company
from .forms import AssetForm

asset_blueprint = Blueprint(
    'asset',
    __name__,
    template_folder='../templates/sistema/asset',
    url_prefix="/system"
)


@asset_blueprint.route('/asset_list', methods=['GET', 'POST'])
@login_required
def list():
    assets = Asset.query.order_by(Asset.short_description.asc())
    return render_template('asset_list.html', assets=assets)


# @asset_blueprint.route('/asset', methods=['GET', 'POST'])
# @login_required
# def new():
#     form = AssetForm()
#     asset = Asset()
#     asset.id = 0
#     if form.validate_on_submit():
#         form.populate_obj(asset)
#         db.session.add(asset)
#         db.session.commit()
#         flash("Equipamento cadastrado", category="success")
#         return redirect(url_for("asset.list"))
#     return render_template("asset_edit.html", form=form, asset=asset)


# @asset_blueprint.route('/asset/<int:id>', methods=['GET', 'POST'])
# @login_required
# def asset(id):
#     asset = Asset.query.filter_by(id=id).first()
#     if asset:
#         form = AssetForm(obj=asset)
#
#         if form.validate_on_submit():
#             form.populate_obj(asset)
#             db.session.add(asset)
#             db.session.commit()
#             flash("Equipamento atualizado", category="success")
#             return redirect(url_for("asset.list"))
#     else:
#         flash("Equipamento não cadastrado", category="danger")
#         return redirect(url_for("asset.list"))
#     return render_template("asset_edit.html", form=form, asset=asset)


@asset_blueprint.route('/asset/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if id > 0:
        # Atualizar
        asset = Asset.query.filter_by(id=id).first()
        form = AssetForm(obj=asset)
        new = False
    else:
        # Cadastrar
        asset = Asset()
        asset.id = 0
        form = AssetForm()
        new = True

    # Listas
    form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]

    # Validação
    if form.validate_on_submit():
        asset.change_attributes(form, new)
        db.session.add(asset)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Equipamento atualizado", category="success")
        else:
            flash("Equipamento cadastrado", category="success")

        return redirect(url_for("asset.list"))
    return render_template("asset_edit.html", form=form, asset=asset)


@asset_blueprint.route('/active_asset/<int:id>', methods=['GET', 'POST'])
@login_required
def active(id):
    asset_ = Asset.query.filter_by(id=id).one()
    if asset_:
        asset_.change_active()
        db.session.add(asset_)
        db.session.commit()
    return redirect(url_for('asset.list'))
