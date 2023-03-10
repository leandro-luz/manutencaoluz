import config
from flask import (render_template, Blueprint,
                   redirect, jsonify, url_for,
                   flash)
from flask_login import current_user, login_required
from webapp.company.models import db, Lead, Companytype, Company, Business, Subbusiness
from webapp.company.forms import CompanyForm, BusinessForm, SubbusinessForm, RegisterForm
from webapp.plan.models import Plan
from webapp.auth.models import Password, User, Role, ViewRole
from webapp.plan.models import ViewPlan
from webapp.auth import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token

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
        # instância uma empresa com base no idenfificador
        company_ = Company.query.filter_by(id=company_id).first()
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

    # atribuindo o tipo "Cliente" para a empresa
    companytype = Companytype.query.filter_by(name='Cliente').one_or_none
    company_.companytype_id = companytype.id

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():
        company_.change_attributes(form, current_user.company_id, new)
        company_.save()

        if new:
            company_ = Company.query.filter_by(name=form.name.data).one()
            new_admin(company_)
            flash("Usuário cadastrado com sucesso, informações de acesso enviadas ao email", category="success")
            # else:
            #     flash("Erro ao cadastrar o usuário do sistema", category="danger")
        # --------- MENSAGENS
        if company_id > 0:
            flash("Empresa atualizada", category="success")
        else:
            flash("Empresa cadastrada", category="success")

        return redirect(url_for("company.company_list"))
    return render_template("company_edit.html", form=form, company=company_)


def new_admin(company: [Company]):
    """    Função para cadastrar os administradores do sistema das empresas    """
    # lista dos administradores
    lista = [{'name': 'admin_', 'email': company.email, 'temporary': True},
             {'name': 'adminluz_', 'email': config.Config.MAIL_USERNAME, 'temporary': False},
             ]
    # laço de repetição
    for valor in lista:
        # cadastro da regra
        role = Role(name='admin', description='administrador', company_id=company.id)
        role.save()

        # busca a lista de telas liberadas para a empresa
        viewplans = ViewPlan.query.filter_by(plan_id=company.plan_id).all()
        for viewplan in viewplans:
            # cadastro de viewroles para o administrador
            viewrole = ViewRole(role_id=role.id, view_id=viewplan.view_id, active=viewplan.active)
            viewrole.save()

        # instância um novo objeto password_
        password_ = Password()
        if valor['temporary']:
            # informa a senha de administrador do sistema, a senha não expira
            password_.set_password(Password.password_random())
            password_.set_expirate(False)
        else:
            # informa uma senha temporária para o administrador da empresa, e informa a data de expiração da senha
            password_.set_password(Password.password_adminluz())
            password_.set_expiration_date()
            password_.set_temporary(False)
        password_.save()

        # instância um novo objeto usuário
        user = User()
        # cria os usuários administradores do sistema para a nova empresa
        user.user_admin(name=valor['name']+company.name, email=valor['email'], company_id=company.id,
                        role_id=role.id, password_=password_.id)

        if user.save():
            # envia o email com as informações de login
            send_email(valor['email'],
                       'Manutenção Luz - Informações para login',
                       'auth/email/confirm',
                       user=user)


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
    # retorna uma lista de subnegócios
    subbusinesss = Subbusiness.query.order_by(Subbusiness.business_id.asc())
    return render_template('subbusiness_list.html', subbusinesss=subbusinesss)


@company_blueprint.route('/subbusiness/<int:subbusiness_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_edit(subbusiness_id: int):
    """    Função que edita as informações do subnegócio    """
    if subbusiness_id > 0:  # se o identificador foi passado como parâmetro
        #  --------- ATUALIZAR
        # retorna uma lista de subnegócio com base no subbusiness_id
        subbusiness = Subbusiness.query.filter_by(id=subbusiness_id).first()
        # instância um formulário e coloca as informações do formulário
        form = SubbusinessForm(obj=subbusiness)

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


@company_blueprint.route('/request', methods=['GET', 'POST'])
def request():
    form = RegisterForm()
    if form.validate_on_submit():
        lead = Lead()
        lead.change_attributes(form)
        if lead.save():
            flash("Informações enviadas com sucesso, em breve vamos lhe atender", category="success")

        return redirect(url_for('main.index'))
    return render_template('company_request.html', form=form)


@company_blueprint.route('/lead_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def lead_list() -> str:
    """    Função que retorna uma lista com interessados     """
    # retorna uma lista de interessados
    leads = Lead.query.order_by(Lead.data_solicitacao.desc())
    return render_template('lead_list.html', leads=leads)


@company_blueprint.route('/enviar_link/<int:lead_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def enviar_link(lead_id):
    lead = Lead.query.filter_by(id=lead_id).first()
    try:
        token = create_token(lead.id, lead.email)
        send_email(lead.email,
                   'Solicitação de acesso',
                   'company/email/proposta',
                   lead=lead,
                   token=token)
        flash(f'Foi enviado para o email as propostas de cadastro para a empresa {lead.name}', category="success")
    except:
        flash("Erro ao enviar o link para o lead", category="danger")
    return redirect(url_for('company.lead_list'))


@company_blueprint.route('/lead_confirm/<token>', methods=['GET', 'POST'])
def lead_confirm(token):
    """    Função de confirmação do token do lead    """
    # consulta as informações do token enviado
    result, lead_id = verify_token("id", token)
    # se o token está válido
    if result:
        # instância um novo lead
        lead = Lead.query.filter_by(id=lead_id).one_or_none()
        # cria um novo token de segurança
        token = create_token(lead.id, lead.email)
        # cria uma empresa e importa as informações do lead
        company = Company()
        company.import_lead(lead)
        # instânciar o formulário com as informações inicias do interessado
        form = CompanyForm(obj=company)
        # --------- LISTAS
        form.business.choices = [(business.id, business.name) for business in Business.query.all()]
        form.subbusiness.choices = [(subbusiness.id, subbusiness.name)
                                    for subbusiness in Subbusiness.query.filter_by(business_id=1)]
        form.plan.choices = [(plans.id, plans.name) for plans in Plan.query.all()]

        # redireciona para a tela de registro de empresa, usando token
        return render_template('company_register.html', form=form, token=token)
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@company_blueprint.route('/company_register/<token>', methods=['GET', 'POST'])
def company_register(token):
    """    Função que grava as informações de um cadastro empresa externo    """
    # consulta as informações do token enviado
    result, lead_id = verify_token("id", token)
    form = CompanyForm()
    # se o token está válido
    if result:
        if form.validate_on_submit():
            new = True
            company_ = Company()
            company_.change_attributes(form, 1, new)
            # atribuindo o tipo "Cliente" para a empresa
            companytype = Companytype.query.filter_by(name='Cliente').one_or_none()
            company_.companytype_id = companytype.id

            if company_.save():
                # instância um lead
                lead = Lead.query.filter_by(id=lead_id).one_or_none()
                # registra o lead como cadastrado
                lead.registred()
                # criar os admnistradores para a empresa
                new_admin(company_)
                flash("Usuário cadastrado com sucesso, informações de acesso enviadas ao email", category="success")
                return redirect(url_for('auth.login'))
                # else:
                #     flash("Erro ao cadastrar o usuário do sistema", category="danger")
                #     return redirect(url_for('main.index'))
        else:
            flash("O cadastro não foi realizado", category="danger")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))
