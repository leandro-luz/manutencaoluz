from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.auth.models import db, Password, User, Role, ViewRole
from webapp.plan.models import ViewPlan
from webapp.company.models import Company
from .forms import LoginForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm, EditForm, \
    RoleForm, ViewRoleForm
from webapp.auth import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token
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
        # if not current_user.confirmed \
        #         and request.endpoint \
        #         and request.blueprint != 'auth' \
        #         and request.endpoint != 'static':
        #     return redirect(url_for('auth.unconfirmed'))


# @auth_blueprint.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('main.index'))
#     return redirect(url_for('auth.login'))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """    Função para logar o usuário no sistema    """
    # instância um formulário vazio
    form = LoginForm()
    # valida as informações passadas
    if form.validate_on_submit():
        user_ = User.query.filter_by(username=form.username.data).one_or_none()
        if user_:
            login_user(user_)
            return redirect(url_for('sistema.index'))
        else:
            flash("Erro ao logar o usuário no sistema.", category="danger")
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @auth_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         new_user = User(form.username.data.lower())
#         new_user.set_email(form.email.data.lower())
#         new_user.set_password(form.password.data)
#         db.session.add(new_user)
#         db.session.commit()
#         token = new_user.create_token()
#         send_email(new_user.email,
#                    'Confirmação de Conta',
#                    'auth/email/confirm',
#                    user=new_user,
#                    token=token)
#         flash("Para finalizar o cadastro, foi enviado a confirmação para o seu email.", category="success")
#         return redirect(url_for('.login'))
#     return render_template('register.html', form=form)


# @auth_blueprint.route('/confirm/<token>')
# def confirm(token):
#     result, user_id = verify_token("id", token)
#     if result:
#         user_ = User.query.filter_by(id=user_id).one()
#         if user_ is not None and not user_.confirmed:
#             user.set_confirmed(True)
#             db.session.add(user_)
#             db.session.commit()
#             flash("Sua conta foi confirmada, Obrigado", category="success")
#             return redirect(url_for('auth.login'))
#         return redirect(url_for('main.index'))
#     else:
#         flash("O link para confirmação é invalido ou está expirado!", category="danger")
#     return redirect(url_for('main.index'))


@auth_blueprint.route('/<string:username>/confirm', methods=['GET', 'POST'])
def resend_confirmation(username):
    user_ = User.query.filter_by(username=username).one()
    token = create_token(user_.id, user_.email)
    send_email(user_.email,
               'Confirmação de Conta',
               'auth/email/confirm',
               user=user_,
               token=token)
    flash("Um novo email de confirmação foi enviado para o seu email.", category="warning")
    return redirect(url_for('main.index'))


# alteração de senha quando logado
@auth_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """    Função para alteração de senha de acesso do usuário logado   """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # coleta a senha do usuário logado
        password = Password.query.filter_by(id=current_user.password.id).one_or_none()
        if password:
            # realiza as alterações
            password.change_attributes(form)
            if password.save():

                # enviar email com a senha atualizada
                send_email(current_user.email,
                           'Alteração de Senha',
                           'auth/email/change_password',
                           user=current_user)

                flash("Sua senha foi atualizada", category="success")
                return redirect(url_for('main.index'))
            else:
                flash("Erro ao alterar senha no banco de dados", category="danger")
        else:
            flash("Erro ao alterar senha", category="danger")

    return render_template("auth/change_password.html", form=form)


# solicitação de nova senha
@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user_ = User.query.filter_by(email=form.email.data.lower()).first()
        if user_:
            token = create_token(user_.id, user_.email)
            send_email(user_.email,
                       'Redefinição de Senha',
                       'auth/email/reset_password',
                       user=user_,
                       token=token)
        flash("Um email com instruções para redefinição de senha foi enviado para seu email.",
              category="warning")
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset_verify_token(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    result, user_id = verify_token("id", token)
    if result:
        user_ = User.query.filter_by(id=user_id).one()
        if user_:
            return redirect(url_for('auth.password_reset', token=token))
        return redirect(url_for('main.index'))
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
        return redirect(url_for('main.index'))


@auth_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    result, user_id = verify_token("id", token)
    if result:
        if form.validate_on_submit():
            user_ = User.query.filter_by(id=user_id).one_or_none()
            password = Password.query.filter_by(id=user_id).one_or_none()
            if password:
                password.change_attributes(form)
                if password.save():
                    # enviar email com a senha atualizada
                    send_email(user_.email,
                               'Alteração de Senha',
                               'auth/email/change_password',
                               user=user_)

                    flash("Sua senha foi atualizada.", category="success")
                    return redirect(url_for('auth.login'))
                else:
                    flash("Ocorreu um erro ao tentar atualizar a senha.", category="danger")

            return redirect(url_for('main.index'))
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
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
            token = create_token(current_user.id, current_user.email)
            send_email(form.email.data.lower(),
                       'Confirme seu novo email',
                       'auth/email/change_email',
                       user=current_user,
                       token=token)
            flash("Foi enviado um email com instruções para confirmar seu novo email.", category="warning")
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inválidos", category="danger")
    return render_template("auth/change_email.html", form=form, token=token)


@auth_blueprint.route('/change_email/<token>')
@login_required
def change_email(token):
    result, email = verify_token("email", token)
    if result:
        user_ = User.query.filter_by(id=current_user.id).one_or_none()
        user_.set_email(email)
        if user_.save():
            flash("Seu email foi atualizado.", category="success")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/auth_active/<int:user_id>')
@login_required
def auth_active(user_id):
    """    Função que ativa/inativa um usuário"""
    user_ = User.query.filter_by(id=user_id).one()  # retorna o usuário com o identificador
    if user_:  # se o usuário existir
        user_.change_active()  # grava as informações vindas do formulário
        user_.save()  # grava as informações no banco de dados
    else:  # se o usuário não existir
        flash("Usuário não cadastrado", category="danger")
    return redirect(url_for('.list'))


@auth_blueprint.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def user(id):
    user_ = User.query.filter_by(id=id).one_or_none()
    if user_:
        return render_template('user.html', user=user_)
    flash("Usuário não cadastrado", category="danger")


@auth_blueprint.route('/auth_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_list() -> str:
    """    Função que retorna uma lista de usuários    """
    # retorna uma lista de usuários da empresa, exceto os adminluz(administradores de sistema)
    users = User.query.filter_by(company_id=current_user.company_id).\
        filter(User.username.notlike("%adminluz%")).all()

    return render_template('user_list.html', users=users)


@auth_blueprint.route('/auth_edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_edit(user_id):
    """    Função atualiza as informações do usuário    """
    if user_id > 0:  # se o identificador foi passado com parâmetro
        # --------- ATUALIZAR
        user_ = User.query.filter_by(id=user_id).first()  # instância um usuário com base no identificador
        form = EditForm(obj=user_)  # instância um formulário com as informações do usuário
        new = False  # não é um usuário novo

        # --------- ATUALIZAR/LER OS DADOS
        if form.company.data:
            c_d = form.company.data
            r_d = form.role.data
        else:
            c_d = user_.company_id
            r_d = user_.role_id

    else:
        # --------- CADASTRAR
        user_ = User()  # instância um usuário em branco
        user_.id = 0
        form = EditForm()  # instância um formulário em branco
        new = True  # é um usuário novo
        c_d = form.company.data
        r_d = form.role.data

    # --------- LISTAS

    form.company.choices = [(companies.id, companies.name) for companies
                            in Company.query.filter_by(id=current_user.company_id).all()]
    # perfil superadmin
    # form.company.choices = [(companies.id, companies.name) for companies in Company.query.all()]
    form.company.data = c_d

    form.role.choices = [(roles.id, roles.name) for roles
                         in Role.query.filter_by(company_id=current_user.company_id).
                             filter(Role.name.notlike("%adminluz%")).all()]
    form.role.data = r_d

    # --------- VALIDAÇÕES
    if form.validate_on_submit():

        if new:
            # instância um novo objeto password_
            password_ = Password()
            password_.set_password(Password.password_random())
            password_.set_expiration_date()
            password_.save()
            user_.password_id = password_.id
        # grava as informações do formulário no objeto usuário
        user_.change_attributes(form, new)
        user_.save()
        if new:
            # envia o email com as informações de login
            send_email(user_.email,
                       'Manutenção Luz - Informações para login',
                       'auth/email/confirm',
                       user=user_)
            flash("Usuário cadastrado", category="success")
        else:
            flash("Usuário atualizado", category="success")
        # else:
        #     flash("Erro ao cadastrar/atualizar usuário", category="danger")

        return redirect(url_for("auth.auth_list"))
    return render_template("user_edit.html", form=form, user=user_)


@auth_blueprint.route('/role_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_list():
    roles = Role.query.filter_by(company_id=current_user.company_id)
    return render_template('role_list.html', roles=roles)


@auth_blueprint.route('/role_edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_edit(role_id):
    if role_id > 0:
        # Atualizar
        role = Role.query.filter_by(id=role_id).first()
        form = RoleForm(obj=role)
        new = False

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

    form.view.choices = [(viewroles.id, viewroles.view.name)
                         for viewroles in ViewRole.query.filter_by(role_id=role_id, active=True).all()]

    # Validação
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
        if role_id > 0:
            flash("Perfil atualizado", category="success")
        else:
            flash("Perfil cadastrado", category="success")

        return redirect(url_for("auth.role_list"))
    return render_template("role_edit.html", form=form, role=role)


@auth_blueprint.route('/viewrole_list/<int:role_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_list(role_id):
    viewroles = ViewRole.query.filter_by(role_id=role_id, active=True).all()
    return render_template('viewrole_list.html', viewroles=viewroles, role_id=role_id)


@auth_blueprint.route('/viewrole_edit/<int:role_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_edit(role_id):
    form = ViewRoleForm()

    form.role.choices = [(roles.id, roles.name) for roles in Role.query.filter_by(id=role_id)]

    form.view.choices = [(viewplans.view.id, viewplans.view.name)
                         for viewplans in ViewPlan.query.filter_by(plan_id=current_user.company.plan_id, active=True)]

    # Validação
    if form.validate_on_submit():
        viewplan = ViewPlan()
        viewplan.change_attributes(form)
        db.session.add(viewplan)
        db.session.commit()

        # Mensagens
        if role_id > 0:
            flash("Tela atualizada", category="success")

        return redirect(url_for("auth.viewrole_list", role_id=role_id))
    return render_template("viewrole_edit.html", form=form, role_id=role_id)


@auth_blueprint.route('/viewrole_active/<int:role_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_active(role_id):
    viewrole = ViewRole.query.filter_by(id=role_id).one()
    if viewrole:
        viewrole.change_active()
        db.session.add(viewrole)
        db.session.commit()
    return redirect(url_for('auth.viewrole_list', role_id=viewrole.role_id))
