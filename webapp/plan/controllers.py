from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import current_user, login_required
from .models import db, Plan, View, ViewPlan
from .forms import PlanForm, ViewForm, ViewPlanForm
from webapp.auth import has_view

plan_blueprint = Blueprint(
    'plan',
    __name__,
    template_folder='../templates/sistema/plan',
    url_prefix="/system"
)


@plan_blueprint.route('/viewplan_active/<int:id>')
@login_required
@has_view('Plano')
def viewplan_active(id):
    viewplan = ViewPlan.query.filter_by(id=id).one()
    if viewplan:
        viewplan.change_active()
        db.session.add(viewplan)
        db.session.commit()
    return redirect(url_for('plan.viewplan_list', id=viewplan.plan_id))


@plan_blueprint.route('/plan_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_list():
    plans = Plan.query.order_by(Plan.name.asc())
    return render_template('plan_list.html', plans=plans)


@plan_blueprint.route('/plan_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_edit(id):
    if id > 0:
        # Atualizar
        plan = Plan.query.filter_by(id=id).first()
        form = PlanForm(obj=plan)
        # new = False

    else:
        # Cadastrar
        plan = Plan()
        plan.id = 0
        form = PlanForm()
        # new = True

    # Listas
    form.view.choices = [(viewplans.id, viewplans.get_name_view(viewplans.view_id)) for viewplans
                         in ViewPlan.query.filter_by(plan_id=id).all()]

    # Validação
    if form.validate_on_submit():
        plan.change_attributes(form)
        db.session.add(plan)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Plano atualizado", category="success")
        else:
            flash("Plano cadastrado", category="success")

        return redirect(url_for("plan.plan_list"))
    return render_template("plan_edit.html", form=form, plan=plan)


@plan_blueprint.route('/viewplan_list/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_list(id):
    plan = Plan.query.filter_by(id=id).one()
    viewplans = ViewPlan.query.filter_by(plan_id=id).all()
    return render_template('viewplan_list.html', viewplans=viewplans, plan=plan)


@plan_blueprint.route('/viewplan_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_edit(id):
    form = ViewPlanForm()

    form.plan.choices = [(plans.id, plans.name) for plans
                         in Plan.query.filter_by(id=id)]

    form.view.choices = [(views.id, views.name) for views in View.query.all()]

    # Validação
    if form.validate_on_submit():
        viewplan = ViewPlan()
        viewplan.change_attributes(form)
        db.session.add(viewplan)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Tela atualizada", category="success")

        return redirect(url_for("plan.viewplan_list", id=id))
    return render_template("viewplan_edit.html", form=form, id=id)


@plan_blueprint.route('/view_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_list():
    views = View.query.order_by(View.plan_id.asc())
    return render_template('view_list.html', views=views)


@plan_blueprint.route('/view_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_edit(id):
    if id > 0:
        # Atualizar
        view = View.query.filter_by(id=id).first()
        form = ViewForm(obj=view)
    else:
        # Cadastrar
        view = View()
        view.id = 0
        form = ViewForm()

    # Validação
    if form.validate_on_submit():
        view.change_attributes(form)
        db.session.add(view)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Tela atualizada", category="success")
        else:
            flash("Tela cadastrada", category="success")

        return redirect(url_for("plan.view_list"))
    return render_template("view_edit.html", form=form, view=view)
