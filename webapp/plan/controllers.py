from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   flash)
from flask_login import login_required
from .models import db, Plan, View, ViewPlan
from webapp.plan.forms import PlanForm, ViewForm, ViewPlanForm
from webapp.company.models import Company
from webapp.auth.models import Role, ViewRole
from webapp.auth import has_view


plan_blueprint = Blueprint(
    'plan',
    __name__,
    template_folder='../templates/sistema/plan',
    url_prefix="/system"
)


@plan_blueprint.route('/plan_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_list() -> str:
    """    Função que retorna uma lista de planos    """
    plans = Plan.query.order_by(Plan.name.asc())  # lista de planos de assinatura em ordem crescente
    return render_template('plan_list.html', plans=plans)


@plan_blueprint.route('/plan_edit/<int:plan_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_edit(plan_id: int):
    """    Função que cadastra ou atualiza um plano de assinatura    """
    if plan_id == 0:
        # --------- CADASTRAR
        plan = Plan()  # instancia um novo plano
        plan.id = 0  # atribui 0 para o id deste novo plano
        form = PlanForm()  # instância um novo formulário

    else:
        # --------- ATUALIZAR
        plan = Plan.query.filter_by(id=plan_id).first()  # gera uma consulta dos planos cadastrados no banco de dados
        form = PlanForm(obj=plan)  # inclui a consulta para dentro do formulário

        # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
        form.view.choices = [(viewplans.id, viewplans.plan.name) for viewplans
                             in ViewPlan.query.filter_by(plan_id=plan_id).all()]  # consulta dos planos com 'id' e nome

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # válida as informações do formulário
        plan.change_attributes(form)  # coleta as informações do formulário e insere no plano
        db.session.add(plan)  # adiciona na sessão
        db.session.commit()  # salva no banco de dados

        # --------- MENSAGENS
        if plan_id > 0:
            flash("Plano atualizado", category="success")
        else:
            flash("Plano cadastrado", category="success")
        return redirect(url_for("plan.plan_list"))  # retorna após o cadastro ou atualização
    return render_template("plan_edit.html", form=form, plan=plan)  # retorna caso não esteja validado por algum motivo


@plan_blueprint.route('/viewplan_list/<int:plan_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_list(plan_id: int) -> str:
    """    Função que retorna uma lista de telas de um plano de assinatura    """
    plan = Plan.query.filter_by(id=plan_id).one()  # instância um plano com base no 'id' de entrada
    viewplans = ViewPlan.query.filter_by(plan_id=plan_id).all()  # busca a lista das telas do plano
    return render_template('viewplan_list.html', viewplans=viewplans, plan=plan)


@plan_blueprint.route('/viewplan_edit/<int:plan_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_edit(plan_id: int):
    """    Função que edita as telas de um plano de assinatura    """
    form = ViewPlanForm()  # instância um formulário de telas de planos de assinatura

    # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
    form.plan.choices = [(plans.id, plans.name) for plans
                         in Plan.query.filter_by(id=plan_id)]  # lista('id' e nome) de planos com base no 'id'

    form.view.choices = [(views.id, views.name) for views in View.query.all()]  # lista(id e nome) de todas as telas /
    # cadastradas

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # se validado
        viewplan = ViewPlan()  # instância uma tela do plano
        viewplan.change_attributes(form)  # altera as informaçoes da tela do plano com base no formulário de entrada
        db.session.add(viewplan)  # adiciona a viewplan na sessão
        db.session.commit()  # grava a viewplan no banco de dados

        ids = [[dict(role_name=roles.name, role_id=roles.id, view_id=viewplan.view_id)
                for roles in Role.list_roles_by_companies(companies.id)]
               for companies in Company.list_companies_by_plan(viewplan.plan_id)]
        # retorna a lista com todos os perfis que contem o plano alterado
        ViewRole.change_roles(viewplan.active, ids)  # libera a tela e/ou inativa as telas para todo os perfis

        # --------- MENSAGENS
        if plan_id > 0:
            flash("Tela atualizada", category="success")
        return redirect(url_for("plan.viewplan_list", plan_id=plan_id))  # retorna após o cadastro ou atualização
    return render_template("viewplan_edit.html", form=form, id=plan_id)  # retorna caso não seja validado


@plan_blueprint.route('/viewplan_active/<int:viewplan_id>')
@login_required
@has_view('Plano')
def viewplan_active(viewplan_id: int):
    """    Função para ativar/desativar a tela de um plano    """
    viewplan = ViewPlan.query.filter_by(id=viewplan_id).one_or_none()  # instância uma tela de um plano a partir do seu

    if viewplan:  # se existir
        viewplan.change_active()  # ativa e inativa a tela dos planos
        db.session.add(viewplan)  # sala na sessão a tela
        db.session.commit()  # grava no banco de dados

        ids = [[dict(role_name=roles.name, role_id=roles.id, view_id=viewplan.view_id)
                for roles in Role.list_roles_by_companies(companies.id)]
               for companies in Company.list_companies_by_plan(viewplan.plan_id)]  # retorna a lista com todos os perfis
        # , que contem o plano alterado
        ViewRole.change_roles(viewplan.active, ids)  # libera a tela e/ou inativa as telas para todo os perfis

    return redirect(url_for('plan.viewplan_list', plan_id=viewplan.plan_id))


@plan_blueprint.route('/view_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_list() -> str:
    """    Função que retorna uma lista de telas em ordem alfabetica    """
    views = View.query.order_by(View.plan_id.asc())  # lista de telas
    return render_template('view_list.html', views=views)


@plan_blueprint.route('/view_edit/<int:view_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_edit(view_id: int):
    """    Função que atualiza uma tela de um plano de assinatura    """
    if view_id > 0:
        # --------- ATUALIZAR
        view = View.query.filter_by(id=view_id).first()  # busca o tela pelo id
        form = ViewForm(obj=view)  # instância um formulário com base na tela
    else:
        # --------- CADASTRAR
        view = View()  # instância uma tela
        view.id = 0  # atualiza o valor do id da tela
        form = ViewForm()  # instância o formulário de tela

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # se estiver validado
        view.change_attributes(form)  # altera as informaçoes da tela com base no formulário de entrada
        db.session.add(view)  # adiciona a tela na sessão
        db.session.commit()  # salva a tela no banco de dados

        # --------- MENSAGENS
        if view_id > 0:
            flash("Tela atualizada", category="success")
        else:
            flash("Tela cadastrada", category="success")
        return redirect(url_for("plan.view_list"))  # retorna após o cadastro ou atualização
    return render_template("view_edit.html", form=form, view=view)  # retorna caso não seja validado por algum motivo
