from flask import (render_template, Blueprint,
                   redirect, request,
                   jsonify, url_for,
                   flash)
from flask_login import current_user, login_required
from webapp.company.models import db, Company, Business, Subbusiness
from webapp.company.forms import CompanyForm, BusinessForm, SubbusinessForm
from webapp.plan.models import Plan
from webapp.auth.models import User, Role, ViewRole
from webapp.plan.models import ViewPlan
from webapp.auth import has_view

company_blueprint = Blueprint(
    'company',
    __name__,
    template_folder='../templates/sistema/company',
    url_prefix="/system"
)


@company_blueprint.route('/company_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_list():
    company_ = Company.query.filter_by(id=current_user.company_id).one()
    companies = Company.query.filter_by(manager_company_id=company_.id)
    return render_template('company_list.html', companies=companies)


@company_blueprint.route('/company/subbusiness_list_option/<int:id>', methods=['GET', 'POST'])
@login_required
def subbusiness_list_option(id):
    subbusinesslist = Subbusiness.query.filter_by(business_id=id).all()
    subbusinessarray = []
    for subbusiness in subbusinesslist:
        subbusinessobj = {}
        subbusinessobj['id'] = subbusiness.id
        subbusinessobj['name'] = subbusiness.name
        subbusinessarray.append(subbusinessobj)
    return jsonify({'subbusiness_list': subbusinessarray})


@company_blueprint.route('/company_active/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_active(id):
    company_ = Company.query.filter_by(id=id).one()
    if company_:
        company_.change_active()
        db.session.add(company_)
        db.session.commit()
    return redirect(url_for('company.list'))


@company_blueprint.route('/company_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_edit(id):
    if id > 0:
        # Ler
        company_ = Company.query.filter_by(id=id).first()
        form = CompanyForm(obj=company_)
        new = False
        subbusiness = Subbusiness.query.filter_by(id=company_.subbusiness_id).one()
        plan = Plan.query.filter_by(id=company_.plan_id).one()

        # Atualizar ou Ler dados
        if form.business.data:
            b_d = form.business.data
            sb_d = form.subbusiness.data
            p_d = form.plan.data
        else:
            b_d = subbusiness.business_id
            sb_d = subbusiness.id
            p_d = plan.id
    else:
        # Cadastrar
        company_ = Company()
        company_.id = 0
        form = CompanyForm()
        new = True
        b_d = 1
        subbusiness = Subbusiness.query.filter_by(business_id=b_d).first()
        sb_d = subbusiness.id
        p_d = form.plan.data

    # Listas
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    form.business.data = b_d

    subbusiness_list = Subbusiness.query.filter_by(business_id=b_d)
    form.subbusiness.choices = [(subbusiness.id, subbusiness.name) for subbusiness in subbusiness_list]
    form.subbusiness.data = sb_d

    form.plan.choices = [(plans.id, plans.name) for plans in Plan.query.all()]
    form.plan.data = p_d

    # Validação
    if form.validate_on_submit():
        company_.change_attributes(form, current_user.company_id, new)
        db.session.add(company_)
        db.session.commit()

        if new:
            company_ = Company.query.filter_by(name=form.name.data).one()
            # cadastro da regra
            role = Role()
            role.name = 'admin'
            role.description = 'administrador'
            role.company_id = company_.id
            db.session.add(role)
            db.session.commit()

            role = Role.query.filter_by(name='admin', company_id=company_.id).one()
            viewplans = ViewPlan.query.filter_by(plan_id=company_.plan_id).all()
            for viewplan in viewplans:
                # cadastro de viewroles para o administrador
                viewrole = ViewRole()
                viewrole.active = True
                viewrole.role_id = role.id
                viewrole.view_id = viewplan.view_id
                db.session.add(viewrole)
                db.session.commit()

            # cadastro do usuario admin
            user = User()
            user.username = 'admin_' + company_.name
            user.email = 'admin' + company_.name + '@admin'
            user.password = 'aaa11111'
            user.company_id = company_.id
            user.role_id = role.id
            user.confirmed = True
            user.active = True
            db.session.add(user)
            db.session.commit()

        # Mensagens
        if id > 0:
            flash("Empresa atualizada", category="success")
        else:
            flash("Empresa cadastrada", category="success")

        return redirect(url_for("company.company_list"))
    return render_template("company_edit.html", form=form, company=company_)


@company_blueprint.route('/business_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def business_list():
    businesss = Business.query.order_by(Business.name.asc())
    return render_template('business_list.html', businesss=businesss)


@company_blueprint.route('/business/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def business_edit(id):
    if id > 0:
        # Atualizar
        business = Business.query.filter_by(id=id).first()
        form = BusinessForm(obj=business)
    else:
        # Cadastrar
        business = Business()
        business.id = 0
        form = BusinessForm()

    # Validação
    if form.validate_on_submit():
        business.change_attributes(form)
        db.session.add(business)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Ramo de negócios atualizado", category="success")
        else:
            flash("Ramo de negócios cadastrado", category="success")

        return redirect(url_for("company.business_list"))
    return render_template("business_edit.html", form=form, business=business)


@company_blueprint.route('/subbusiness_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_list():
    subbusinesss = Subbusiness.query.order_by(Subbusiness.business_id.asc())
    return render_template('subbusiness_list.html', subbusinesss=subbusinesss)


@company_blueprint.route('/subbusiness/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_edit(id):
    if id > 0:
        # Atualizar
        subbusiness = Subbusiness.query.filter_by(id=id).first()
        form = SubbusinessForm(obj=subbusiness)

        # Atualizar ou Ler dados
        if form.business.data:
            b_d = form.business.data
        else:
            b_d = subbusiness.business_id

    else:
        # Cadastrar
        subbusiness = Subbusiness()
        subbusiness.id = 0
        form = SubbusinessForm()
        b_d = form.business.data

    # Listas
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    form.business.data = b_d

    # Validação
    if form.validate_on_submit():
        subbusiness.change_attributes(form)
        db.session.add(subbusiness)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Sub-Ramo de negócios atualizado", category="success")
        else:
            flash("Sub-Ramo de negócios cadastrado", category="success")

        return redirect(url_for("company.subbusiness_list"))
    return render_template("subbusiness_edit.html", form=form, subbusiness=subbusiness)
