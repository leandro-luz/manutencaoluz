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
    url_prefix="/sistema"
)


@company_blueprint.route('/company_list', methods=['GET', 'POST'])
@login_required
def list():
    companies = Company.query.order_by(Company.name.asc())
    return render_template('company_list.html', companies=companies)


@company_blueprint.route('/company_new', methods=['GET', 'POST'])
@login_required
def new():
    form = CompanyForm()
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    business = Business.query.first()
    subbusiness_list = Subbusiness.query.filter_by(business_id=business.id)
    form.subbusiness.choices = [(subbusiness.id, subbusiness.name) for subbusiness in subbusiness_list]
    if form.validate_on_submit():
        company_ = Company()
        company_.setName(form.name.data)
        company_.setCnpj(form.cnpj.data)
        company_.setCep(form.cep.data)
        company_.setEmail(form.email.data)
        company_.setActive(form.active.data)
        company_.setSubbsiness(form.subbusiness.data)
        company_.setMemberSince()
        db.session.add(company_)
        db.session.commit()
        flash("Empresa adcionada", category="success")
        return redirect(url_for("company.list"))

    return render_template("company_new.html", form=form)


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


@company_blueprint.route('/company/<int:id>', methods=['GET', 'POST'])
@login_required
def company(id):
    company_ = Company.query.filter_by(id=id).one()
    subbusiness = Subbusiness.query.filter_by(id=company_.subbusiness_id).one()
    business = Business.query.filter_by(id=subbusiness.business_id).one()
    if company_:
        return render_template('company.html', company=company_,
                               subbusiness=subbusiness, business=business)
    flash("Empresa não cadastrada", category="danger")


@company_blueprint.route('/active/<int:id>', methods=['GET', 'POST'])
@login_required
def active(id):
    company_ = Company.query.filter_by(id=id).one()
    if company_:
        company_.changeActive()
        db.session.add(company_)
        db.session.commit()
    return redirect(url_for('company.list'))


@company_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    company_ = Company.query.filter_by(id=id).one()
    form = CompanyForm(obj=company_)
    # form = CompanyForm()
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    business = Business.query.first()
    subbusiness_list = Subbusiness.query.filter_by(business_id=business.id)
    form.subbusiness.choices = [(subbusiness.id, subbusiness.name) for subbusiness in subbusiness_list]


    if form.validate_on_submit():
        form.populate_obj(company_)
        db.session.add(company_)
        db.session.commit()
        flash("Empresa atualizada", category="success")
        return redirect(url_for("company.company", id=company_.id))
    return render_template("company_edit.html", form=form, company=company_)
