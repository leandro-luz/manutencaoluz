from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.auth.models import db, User, Role, ViewRole
from webapp.plan.models import View, ViewPlan
from webapp.company.models import Company
from webapp.email import send_email
from .forms import LoginForm, RegisterForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm, EditForm, \
    RoleForm, ViewRoleForm
from webapp.auth import has_view

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/system"
)


@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        if user.confirmed:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('sistema.index'))
        return render_template('unconfirmed.html', user=user)
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data.lower())
        new_user.set_email(form.email.data.lower())
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.create_token()
        send_email(new_user.email,
                   'Confirma????o de Conta',
                   'auth/email/confirm',
                   user=new_user,
                   token=token)
        flash("Para finalizar o cadastro, foi enviado a confirma????o para o seu email.", category="success")
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@auth_blueprint.route('/confirm/<token>')
def confirm(token):
    result, user_id = User.verify_token("id", token)
    if result:
        user = User.query.filter_by(id=user_id).one()
        if user is not None and not user.confirmed:
            user.set_confirmed(True)
            db.session.add(user)
            db.session.commit()
            flash("Sua conta foi confirmada, Obrigado", category="success")
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    else:
        flash("O link para confirma????o ?? invalido ou est?? expirado!", category="danger")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/<string:username>/confirm', methods=['GET', 'POST'])
def resend_confirmation(username):
    user = User.query.filter_by(username=username).one()
    token = user.create_token()
    send_email(user.email,
               'Confirma????o de Conta',
               'auth/email/confirm',
               user=user,
               token=token)
    flash("Um novo email de confirma????o foi enviado para o seu email.", category="warning")
    return redirect(url_for('main.index'))


# altera????o de senha quando logado
@auth_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Sua senha foi atualizada", category="success")
            return redirect(url_for('main.index'))
        else:
            flash("Senha inv??lida", category="danger")
    return render_template("auth/change_password.html", form=form)


# solicita????o de nova senha
@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.create_token()
            send_email(user.email,
                       'Redefini????o de Senha',
                       'auth/email/reset_password',
                       user=user,
                       token=token)
        flash("Um email com instru????es para redefini????o de senha foi enviado para seu email.",
              category="warning")
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset_verify_token(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    result, user_id = User.verify_token("id", token)
    if result:
        user = User.query.filter_by(id=user_id).one()
        if user:
            return redirect(url_for('auth.password_reset', token=token))
        return redirect(url_for('main.index'))
    else:
        flash("O link para confirma????o ?? invalido ou est?? expirado!", category="danger")
        return redirect(url_for('main.index'))


@auth_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        result, user_id = User.verify_token("id", token)
        if result:
            user = User.query.filter_by(id=user_id).one()
            if user:
                user.set_password(form.password.data)
                db.session.commit()
                flash("Sua senha foi atualizada.", category="success")
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash("O link para confirma????o ?? invalido ou est?? expirado!", category="danger")
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, token=token)


@auth_blueprint.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    token = ""
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.set_email(form.email.data.lower())
            token = current_user.create_token()
            send_email(form.email.data.lower(),
                       'Confirme seu novo email',
                       'auth/email/change_email',
                       user=current_user,
                       token=token)
            flash("Foi enviado um email com instru????es para confirmar seu novo email.", category="warning")
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inv??lidos", category="danger")
    return render_template("auth/change_email.html", form=form, token=token)


@auth_blueprint.route('/change_email/<token>')
@login_required
def change_email(token):
    result, email = current_user.verify_token("email", token)
    if result:
        current_user.set_email(email)
        db.session.add(current_user)
        db.session.commit()
        flash("Seu email foi atualizado.", category="success")
    else:
        flash("O link para confirma????o ?? invalido ou est?? expirado!", category="danger")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/auth_active/<int:id>')
@login_required
def auth_active(id):
    user = User.query.filter_by(id=id).one()
    if user:
        user.change_active()
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('.list'))


@auth_blueprint.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user = User.query.filter_by(id=id).one()
    if user:
        return render_template('user.html', user=user)
    flash("Usu??rio n??o cadastrado", category="danger")


@auth_blueprint.route('/auth_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_list():
    users = User.query.filter_by(company_id=current_user.company_id).all()
    return render_template('user_list.html', users=users)


@auth_blueprint.route('/auth_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_edit(id):
    if id > 0:
        # Atualizar
        user = User.query.filter_by(id=id).first()
        form = EditForm(obj=user)
        new = False

        # Atualizar ou Ler dados
        if form.company.data:
            c_d = form.company.data
            r_d = form.role.data
        else:
            c_d = user.company_id
            r_d = user.role_id

    else:
        # Cadastrar
        user = User()
        user.id = 0
        form = EditForm()
        new = True
        c_d = form.company.data
        r_d = form.role.data

    # Listas

    form.company.choices = [(companies.id, companies.name) for companies
                            in Company.query.filter_by(id=current_user.company_id).all()]
    ##perfil superadmin
    # form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]
    form.company.data = c_d

    form.role.choices = [(roles.id, roles.name) for roles
                         in Role.query.filter_by(company_id=current_user.company_id).all()]
    form.role.data = r_d

    # Valida????o
    if form.validate_on_submit():
        user.change_attributes(form, new)
        db.session.add(user)
        db.session.commit()

        # Mensagens
        if id > 0:
            flash("Usu??rio atualizado", category="success")
        else:
            flash("Usu??rio cadastrado", category="success")

        return redirect(url_for("auth.auth_list"))
    return render_template("user_edit.html", form=form, user=user)


@auth_blueprint.route('/role_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_list():
    roles = Role.query.filter_by(company_id=current_user.company_id)
    return render_template('role_list.html', roles=roles)


@auth_blueprint.route('/role_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_edit(id):
    if id > 0:
        # Atualizar
        role = Role.query.filter_by(id=id).first()
        form = RoleForm(obj=role)

        # Atualizar ou Ler dados
        if form.company.data:
            b_d = form.company.data
        else:
            b_d = role.company_id

    else:
        # Cadastrar
        role = Role()
        role.id = 0
        form = RoleForm()
        b_d = form.company.data
        new = True

    # Listas
    form.company.choices = [(company.id, company.name)
                            for company in Company.query.filter_by(id=current_user.company_id)]
    form.company.data = b_d

    form.view.choices = [(viewroles.id, viewroles.get_name_view(viewroles.view_id))
                         for viewroles in ViewRole.query.filter_by(role_id=id, active=True).all()]

    # Valida????o
    if form.validate_on_submit():
        role.change_attributes(form)
        db.session.add(role)
        db.session.commit()

        if new:
            role = Role.query.filter_by(name=form.name.data, company_id=form.company.data).one()
            company = Company.query.filter_by(id=b_d).one()
            viewplans = ViewPlan.query.filter_by(plan_id=company.plan_id).all()

            for viewplan in viewplans:
                viewrole = ViewRole()
                viewrole.active = False
                viewrole.role_id = role.id
                viewrole.view_id = viewplan.view_id
                db.session.add(viewrole)
                db.session.commit()

        # Mensagens
        if id > 0:
            flash("Perfil atualizado", category="success")
        else:
            flash("Perfil cadastrado", category="success")

        return redirect(url_for("auth.role_list"))
    return render_template("role_edit.html", form=form, role=role)


@auth_blueprint.route('/viewrole_list/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_list(id):
    viewroles = ViewRole.query.filter_by(role_id=id).all()
    return render_template('viewrole_list.html', viewroles=viewroles)


@auth_blueprint.route('/viewrole_edit/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_edit(id):
    form = ViewRoleForm()

    # form.role.choices = [(role.id, role.name) for plans
    #                      in Plan.query.filter_by(id=id)]

    form.view.choices = [(views.id, views.name) for views in View.query.all()]

    # Valida????o
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


@auth_blueprint.route('/viewrole_active/<int:id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_active(id):
    viewrole = ViewRole.query.filter_by(id=id).one()
    if viewrole:
        viewrole.change_active()
        db.session.add(viewrole)
        db.session.commit()
    return redirect(url_for('auth.viewrole_list', id=viewrole.role_id))
