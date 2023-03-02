from flask import (render_template, Blueprint,
                   redirect, jsonify, url_for,
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
def company_list() -> str:
    """    Retorna a lista de empresas vinculada a empresa do usuario     """
    companies = Company.query.filter_by(manager_company_id=current_user.company_id)  # retorna uma lista com base no _
    # identificador da empresa do usuário
    return render_template('company_list.html', companies=companies)


@company_blueprint.route('/company/subbusiness_list_option/<int:business_id>', methods=['GET', 'POST'])
@login_required
def subbusiness_list_option(business_id: int):
    """    Função que retorna lista de subnegócios"""
    subbusinesslist = Subbusiness.query.filter_by(business_id=business_id).all()  # retorna uma lista de subnegócios _
    # com base no identificador
    subbusinessarray = []
    for subbusiness in subbusinesslist:
        subbusinessobj = {'id': subbusiness.id, 'name': subbusiness.name}
        subbusinessarray.append(subbusinessobj)
    return jsonify({'subbusiness_list': subbusinessarray})


@company_blueprint.route('/company_active/<int:company_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_active(company_id):
    """    Função que ativa/desativa uma empresa    """
    company_ = Company.query.filter_by(id=company_id).one_or_none()  # instância uma empresa com base no identificador
    if company_:  # se a empresa existir
        company_.change_active()  # ativa/inativa a empresa
        company_.save()  # salva no banco de dados a alteração
    else:
        flash("Empresa não registrada", category="danger")
    return redirect(url_for('company.company_list'))


@company_blueprint.route('/company_edit/<int:company_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_edit(company_id):
    """   Função que altera os valores    """
    if company_id > 0:  # se o identificador foi passado como parâmetro
        # --------- LER
        company_ = Company.query.filter_by(id=company_id).first()  # instância uma empresa com base no idenfificador
        form = CompanyForm(obj=company_)  # instânciar o formulário
        new = False  # não é uma empresa nova

        # buscar os subnegócios da empresa
        subbusiness = Subbusiness.query.filter_by(id=company_.subbusiness_id).one_or_none()

        # instância um plano de assinatura com base no identificador do plano da empres
        plan = Plan.query.filter_by(id=company_.plan_id).one_or_none()

        # --------- ATUALIZAR
        if form.business.data:  # se os dados já foram preenchidos
            b_d = form.business.data
            sb_d = form.subbusiness.data
            p_d = form.plan.data
        else:  # pegar os dados selecionados
            b_d = subbusiness.business_id
            sb_d = subbusiness.id
            p_d = plan.id
    else:
        # --------- CADASTRAR
        company_ = Company()  # instânciar o objeto empresa
        company_.id = 0  # informar o id como 0
        form = CompanyForm()  # instânciar o formulário para empresa
        new = True  # é uma empresa nova
        b_d = 1
        subbusiness = Subbusiness.query.filter_by(business_id=b_d).first()
        sb_d = subbusiness.id
        p_d = form.plan.data

    # --------- LISTAS
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    form.business.data = b_d

    form.subbusiness.choices = [(subbusiness.id, subbusiness.name)
                                for subbusiness in Subbusiness.query.filter_by(business_id=b_d)]
    form.subbusiness.data = sb_d

    form.plan.choices = [(plans.id, plans.name) for plans in Plan.query.all()]
    form.plan.data = p_d

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():
        company_.change_attributes(form, current_user.company_id, new)
        company_.save()

        if new:
            company_ = Company.query.filter_by(name=form.name.data).one()
            # cadastro da regra
            role = Role(name='admin', description='administrador', company_id=company_.id)
            role.save()
            viewplans = ViewPlan.query.filter_by(plan_id=company_.plan_id).all()
            for viewplan in viewplans:
                # cadastro de viewroles para o administrador
                viewrole = ViewRole(role_id=role.id, view_id=viewplan.view_id, active=viewplan.active)
                viewrole.save()

            # cadastro do usuario admin
            user = User()  # instância um novo objeto usuário
            user.user_admin(company_name=company_.name, company_id=company_.id, role_id=role.id)  # altera os dados _
            # para administrador
            user.save()  # salva no banco de dados

        # --------- MENSAGENS
        if company_id > 0:
            flash("Empresa atualizada", category="success")
        else:
            flash("Empresa cadastrada", category="success")

        return redirect(url_for("company.company_list"))
    return render_template("company_edit.html", form=form, company=company_)


@company_blueprint.route('/business_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def business_list() -> str:
    """    Função que retorna uma lista de negócios    """
    businesss = Business.query.order_by(Business.name.asc())
    return render_template('business_list.html', businesss=businesss)


@company_blueprint.route('/business/<int:business_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def business_edit(business_id):
    """    Função para alterações das informações do negócio    """
    if business_id > 0:  # se o identificador for passado como parâmetro
        # --------- ATUALIZAR
        business = Business.query.filter_by(id=business_id).first()  # instância um negócio com base no identificador
        form = BusinessForm(obj=business)  # instância um formulário e colocar as informações do formulário
    else:  # se o identificador não for passado como parâmetro
        # --------- CADASTRAR
        business = Business()  # instância um negócio
        business.id = 0  #
        form = BusinessForm()  # instância um formulário em branco

    # --------- VALIDAÇÕES
    if form.validate_on_submit():
        business.change_attributes(form)  # recupera as informações do formulário
        business.save()  # salva as informações no banco de dados

        # --------- MENSAGENS
        if business_id > 0:
            flash("Ramo de negócios atualizado", category="success")
        else:
            flash("Ramo de negócios cadastrado", category="success")

        return redirect(url_for("company.business_list"))
    return render_template("business_edit.html", form=form, business=business)


@company_blueprint.route('/subbusiness_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_list() -> str:
    """    Função que retorna uma lista com subnegócios     """
    subbusinesss = Subbusiness.query.order_by(Subbusiness.business_id.asc())  # retorna uma lista de subnegócios
    return render_template('subbusiness_list.html', subbusinesss=subbusinesss)


@company_blueprint.route('/subbusiness/<int:subbusiness_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_edit(subbusiness_id: int):
    """    Função que edita as informações do subnegócio    """
    if subbusiness_id > 0:  # se o identificador foi passado como parâmetro
        #  --------- ATUALIZAR
        subbusiness = Subbusiness.query.filter_by(id=subbusiness_id).first()  # retorna uma lista de subnegócio com base
        # no subbusiness_id
        form = SubbusinessForm(obj=subbusiness)  # instância um formulário e coloca as informações do formulário

        # Atualizar ou Ler dados
        if form.business.data:
            b_d = form.business.data
        else:
            b_d = subbusiness.business_id

    else:
        # --------- CADASTRAR
        subbusiness = Subbusiness()  # instância um subnegócio em branco
        subbusiness.id = 0
        form = SubbusinessForm()  # instância um formulário em branco
        b_d = form.business.data

    # --------- LISTAS
    form.business.choices = [(business.id, business.name) for business in Business.query.all()]
    form.business.data = b_d

    # --------- VALIDAÇÕES
    if form.validate_on_submit():
        subbusiness.change_attributes(form)
        db.session.add(subbusiness)
        db.session.commit()

        # --------- MENSAGENS
        if subbusiness_id > 0:
            flash("Sub-Ramo de negócios atualizado", category="success")
        else:
            flash("Sub-Ramo de negócios cadastrado", category="success")

        return redirect(url_for("company.subbusiness_list"))
    return render_template("subbusiness_edit.html", form=form, subbusiness=subbusiness)
