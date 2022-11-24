from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import current_user, login_required
from .models import db, Supplier
from webapp.company.models import Company
from webapp.email import send_email
from webapp.auth import has_view

from .forms import SupplierForm

supplier_blueprint = Blueprint(
    'supplier',
    __name__,
    template_folder='../templates/sistema/supplier',
    url_prefix="/system"
)


@supplier_blueprint.route('/supplier_list', methods=['GET', 'POST'])
@login_required
@has_view('Fornecedor')
def supplier_list():
    suppliers = Supplier.query.filter_by(company_id=current_user.company_id).all()
    return render_template('supplier_list.html', suppliers=suppliers)


@supplier_blueprint.route('/supplier_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Fornecedor')
def supplier_edit(id):
    if id > 0:
        # Atualizar
        supplier = Supplier.query.filter_by(id=id).first()
        form = SupplierForm(obj=supplier)

        # Atualizar ou Ler dados
        if form.company.data:
            c_d = form.company.data
        else:
            c_d = supplier.company_id

    else:
        # Cadastrar
        supplier = Supplier()
        supplier.id = 0
        form = SupplierForm()
        c_d = form.company.data

    # Listas
    form.company.choices = [(companies.id, companies.name) for companies
                            in Company.query.filter_by(id=current_user.company_id).all()]
    ##perfil superadmin
    # form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]
    form.company.data = c_d

    # Validação
    if form.validate_on_submit():
        supplier.change_attributes(form)
        db.session.add(supplier)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Fornecedor atualizado", category="success")
        else:
            flash("Fornecedor cadastrado", category="success")

        return redirect(url_for("supplier.supplier_list"))
    return render_template("supplier_edit.html", form=form, supplier=supplier)
