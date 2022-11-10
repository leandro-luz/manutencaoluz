from flask import (render_template, Blueprint,
                   redirect, request,
                   jsonify, url_for,
                   flash)
from flask_login import current_user, login_required
from .models import db, Company, Business, Subbusiness
from .forms import CompanyForm

company_blueprint = Blueprint(
    'company',
    __name__,
    template_folder='../templates/sistema/company',
    url_prefix="/system"
)


@company_blueprint.route('/company_list', methods=['GET', 'POST'])
@login_required
def list():
    companies = Company.query.order_by(Company.name.asc())
    return render_template('company_list.html', companies=companies)


@company_blueprint.route('/subbusiness_list/<int:id>', methods=['GET', 'POST'])
@login_required
def subbusiness_list(id):
    subbusinesslist = Subbusiness.query.filter_by(business_id=id).all()
    subbusinessarray = []
    for subbusiness in subbusinesslist:
        subbusinessobj = {}
        subbusinessobj['id'] = subbusiness.id
        subbusinessobj['name'] = subbusiness.name
        subbusinessarray.append(subbusinessobj)
    return jsonify({'subbusiness_list': subbusinessarray})


@company_blueprint.route('/active_company/<int:id>', methods=['GET', 'POST'])
@login_required
def active(id):
    company_ = Company.query.filter_by(id=id).one()
    if company_:
        company_.change_active()
        db.session.add(company_)
        db.session.commit()
    return redirect(url_for('company.list'))


@company_blueprint.route('/company/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if id > 0:
        # Atualizar
        company_ = Company.query.filter_by(id=id).first()
        form = CompanyForm(obj=company_)
        new = False
    else:
        # Cadastrar
        company_ = Company()
        company_.id = 0
        form = CompanyForm()
        new = True

    # Listas
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    business = Business.query.first()
    subbusiness_list = Subbusiness.query.filter_by(business_id=business.id)
    form.subbusiness.choices = [(subbusiness.id, subbusiness.name) for subbusiness in subbusiness_list]

    #Validação
    if form.validate_on_submit():
        company_.change_attributes(form, new)
        db.session.add(company_)
        db.session.commit()

        #Mensagens
        if id > 0:
            flash("Empresa atualizada", category="success")
        else:
            flash("Empresa cadastrada", category="success")

        return redirect(url_for("company.list"))
    return render_template("company_edit.html", form=form, company=company_)
