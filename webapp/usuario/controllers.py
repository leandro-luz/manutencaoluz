from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.usuario.models import db, Senha, Usuario, Perfil, ViewRole
from webapp.plano.models import Telaplano
from webapp.empresa.models import Empresa
from .forms import LoginForm, AlterarSenhaForm, SolicitarNovaSenhaForm, PasswordResetForm, \
    ChangeEmailForm, EditarUsuarioForm, RoleForm, ViewRoleForm
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token

usuario_blueprint = Blueprint(
    'usuario',
    __name__,
    template_folder='../templates/usuario',
    url_prefix="/sistema"
)


@usuario_blueprint.before_app_request
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


@usuario_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """    Função para logar o usuário no sistema    """
    # instância um formulário vazio
    form = LoginForm()
    # valida as informações passadas
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nome=form.nome.data).one_or_none()
        if usuario:
            login_user(usuario)
            return redirect(url_for('sistema.index'))
        else:
            flash("Erro ao logar o usuário no sistema.", category="danger")
    return render_template('login.html', form=form)


@usuario_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @auth_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistroEmpresaForm()
#     if form.validate_on_submit():
#         new_user = Usuario(form.razao_social.data.lower())
#         new_user.set_email(form.email.data.lower())
#         new_user.set_password(form.senha.data)
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
#         user_ = Usuario.query.filter_by(id=user_id).one()
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


@usuario_blueprint.route('/<string:nome>/confirm', methods=['GET', 'POST'])
def resend_confirmation(nome):
    usuario = Usuario.query.filter_by(nome=nome).one_or_none()
    token = create_token(usuario.id, usuario.email)
    send_email(usuario.email,
               'Confirmação de Conta',
               'usuario/email/confirm',
               usuario=usuario,
               token=token)
    flash("Um novo email de confirmação foi enviado para o seu email.", category="warning")
    return redirect(url_for('main.index'))


# alteração de senha quando logado
@usuario_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """    Função para alteração de senha de acesso do usuário logado   """
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        # coleta a senha do usuário logado
        senha = Senha.query.filter_by(id=current_user.senha.id).one_or_none()
        if senha:
            # realiza as alterações
            senha.alterar_atributos(form)
            if senha.salvar():

                # enviar email com a senha atualizada
                send_email(current_user.email,
                           'Alteração de Senha',
                           'usuario/email/change_password',
                           usuario=current_user)

                flash("Sua senha foi atualizada", category="success")
                return redirect(url_for('main.index'))
            else:
                flash("Erro ao alterar senha no banco de dados", category="danger")
        else:
            flash("Erro ao alterar senha", category="danger")

    return render_template("usuario/change_password.html", form=form)


# solicitação de nova senha
@usuario_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = SolicitarNovaSenhaForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if usuario:
            token = create_token(usuario.id, usuario.email)
            send_email(usuario.email,
                       'Redefinição de Senha',
                       'usuario/email/reset_password',
                       usuario=usuario,
                       token=token)
        flash("Um email com instruções para redefinição de senha foi enviado para seu email.",
              category="warning")
        return redirect(url_for('usuario.login'))
    return render_template('usuario/request_reset_password.html', form=form)


@usuario_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset_verify_token(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    result, user_id = verify_token("id", token)
    if result:
        usuario = Usuario.query.filter_by(id=user_id).one_or_none()
        if usuario:
            return redirect(url_for('usuario.password_reset', token=token))
        return redirect(url_for('main.index'))
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
        return redirect(url_for('main.index'))


@usuario_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    result, user_id = verify_token("id", token)
    if result:
        if form.validate_on_submit():
            usuario = Usuario.query.filter_by(id=user_id).one_or_none()
            senha = Senha.query.filter_by(id=user_id).one_or_none()
            if senha:
                senha.alterar_atributos(form)
                if senha.salvar():
                    # enviar email com a senha atualizada
                    send_email(usuario.email,
                               'Alteração de Senha',
                               'usuario/email/change_password',
                               usuario=usuario)

                    flash("Sua senha foi atualizada.", category="success")
                    return redirect(url_for('usuario.login'))
                else:
                    flash("Ocorreu um erro ao tentar atualizar a senha.", category="danger")

            return redirect(url_for('main.index'))
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
        return redirect(url_for('main.index'))
    return render_template('usuario/reset_password.html', form=form, token=token)


@usuario_blueprint.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    token = ""
    if form.validate_on_submit():
        if current_user.verificar_senha(form.senha.data):
            current_user.alterar_email(form.email.data.lower())
            token = create_token(current_user.id, current_user.email)
            send_email(form.email.data.lower(),
                       'Confirme seu novo email',
                       'usuario/email/change_email',
                       usuario=current_user,
                       token=token)
            flash("Foi enviado um email com instruções para confirmar seu novo email.", category="warning")
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inválidos", category="danger")
    return render_template("usuario/change_email.html", form=form, token=token)


@usuario_blueprint.route('/change_email/<token>')
@login_required
def change_email(token):
    result, email = verify_token("email", token)
    if result:
        usuario = Usuario.query.filter_by(id=current_user.id).one_or_none()
        usuario.alterar_email(email)
        if usuario.salvar():
            flash("Seu email foi atualizado.", category="success")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@usuario_blueprint.route('/auth_active/<int:user_id>')
@login_required
def auth_active(user_id):
    """    Função que ativa/inativa um usuário"""
    usuario = Usuario.query.filter_by(id=user_id).one_or_none()  # retorna o usuário com o identificador
    if usuario:  # se o usuário existir
        usuario.ativar_desativar()  # grava as informações vindas do formulário
        usuario.salvar()  # grava as informações no banco de dados
    else:  # se o usuário não existir
        flash("Usuário não cadastrado", category="danger")
    return redirect(url_for('.list'))


@usuario_blueprint.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user(user_id):
    usuario = Usuario.query.filter_by(id=user_id).one_or_none()
    if usuario:
        return render_template('user.html', usuario=usuario)
    flash("Usuário não cadastrado", category="danger")


@usuario_blueprint.route('/auth_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_list() -> str:
    """    Função que retorna uma lista de usuários    """
    # retorna uma lista de usuários da empresa, exceto os adminluz(administradores de sistema)
    usuarios = Usuario.query.filter_by(empresa_id=current_user.empresa_id).\
        filter(Usuario.nome.notlike("%adminluz%")).all()

    return render_template('user_list.html', usuarios=usuarios)


@usuario_blueprint.route('/auth_edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def auth_edit(user_id):
    """    Função atualiza as informações do usuário    """
    if user_id > 0:  # se o identificador foi passado com parâmetro
        # --------- ATUALIZAR
        usuario = Usuario.query.filter_by(id=user_id).first()  # instância um usuário com base no identificador
        form = EditarUsuarioForm(obj=usuario)  # instância um formulário com as informações do usuário
        new = False  # não é um usuário novo

        # --------- ATUALIZAR/LER OS DADOS
        if form.empresa.data:
            c_d = form.empresa.data
            r_d = form.perfil.data
        else:
            c_d = usuario.empresa_id
            r_d = usuario.perfil_id

    else:
        # --------- CADASTRAR
        usuario = Usuario()  # instância um usuário em branco
        usuario.id = 0
        form = EditarUsuarioForm()  # instância um formulário em branco
        new = True  # é um usuário novo
        c_d = form.empresa.data
        r_d = form.perfil.data

    # --------- LISTAS

    form.empresa.choices = [(companies.id, companies.razao_social) for companies
                            in Empresa.query.filter_by(id=current_user.empresa_id).all()]

    form.empresa.data = c_d

    form.perfil.choices = [(perfis.id, perfis.nome) for perfis in
                           Perfil.query.filter_by(empresa_id=current_user.empresa_id).filter(Perfil.nome.notlike("%adminluz%")).all()]
    form.perfil.data = r_d

    # --------- VALIDAÇÕES
    if form.validate_on_submit():

        if new:
            # instância um novo objeto password_
            password_ = Senha()
            password_.alterar_senha(Senha.senha_aleatoria())
            password_.alterar_data_expiracao()
            password_.salvar()
            usuario.senha_id = password_.id
        # grava as informações do formulário no objeto usuário
        usuario.alterar_atributos(form, new)
        usuario.save()
        if new:
            # envia o email com as informações de login
            send_email(usuario.email,
                       'Manutenção Luz - Informações para login',
                       'usuario/email/confirm',
                       usuario=usuario)
            flash("Usuário cadastrado", category="success")
        else:
            flash("Usuário atualizado", category="success")
        # else:
        #     flash("Erro ao cadastrar/atualizar usuário", category="danger")

        return redirect(url_for("usuario.auth_list"))
    return render_template("user_edit.html", form=form, usuario=usuario)


@usuario_blueprint.route('/role_list', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_list():
    perfis = Perfil.query.filter_by(empresa_id=current_user.empresa_id)
    return render_template('role_list.html', perfis=perfis)


@usuario_blueprint.route('/role_edit/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def role_edit(perfil_id):
    if perfil_id > 0:
        # Atualizar
        perfil = Perfil.query.filter_by(id=perfil_id).first()
        form = RoleForm(obj=perfil)
        new = False

        # Atualizar ou Ler dados
        if form.empresa.data:
            b_d = form.empresa.data
        else:
            b_d = perfil.empresa_id

    else:
        # Cadastrar
        perfil = Perfil()
        perfil.id = 0
        form = RoleForm()
        b_d = form.empresa.data
        new = True

    # Listas
    form.empresa.choices = [(empresa.id, empresa.razao_social)
                            for empresa in Empresa.query.filter_by(id=current_user.empresa_id)]
    form.empresa.data = b_d

    form.tela.choices = [(viewroles.id, viewroles.tela.nome)
                         for viewroles in ViewRole.query.filter_by(perfil_id=perfil_id, active=True).all()]

    # Validação
    if form.validate_on_submit():
        perfil.alterar_atributos(form)
        db.session.add(perfil)
        db.session.commit()

        if new:
            perfil = Perfil.query.filter_by(nome=form.nome.data, empresa_id=form.empresa.data).one_or_none()
            empresa = Empresa.query.filter_by(id=b_d).one_or_none()
            telasplano = Telaplano.query.filter_by(plano_id=empresa.plano_id).all()

            for telaplano in telasplano:
                viewrole = ViewRole()
                viewrole.active = False
                viewrole.perfil_id = perfil.id
                viewrole.tela_id = telaplano.tela_id
                db.session.add(viewrole)
                db.session.commit()

        # Mensagens
        if perfil_id > 0:
            flash("Perfil atualizado", category="success")
        else:
            flash("Perfil cadastrado", category="success")

        return redirect(url_for("usuario.role_list"))
    return render_template("role_edit.html", form=form, perfil=perfil)


@usuario_blueprint.route('/viewrole_list/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_list(perfil_id):
    viewroles = ViewRole.query.filter_by(perfil_id=perfil_id, active=True).all()
    return render_template('viewrole_list.html', viewroles=viewroles, perfil_id=perfil_id)


@usuario_blueprint.route('/viewrole_edit/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_edit(perfil_id):
    form = ViewRoleForm()

    form.perfil.choices = [(perfis.id, perfis.nome) for perfis in Perfil.query.filter_by(id=perfil_id)]

    form.tela.choices = [(telasplano.tela.id, telasplano.tela.nome)
                         for telasplano in Telaplano.query.filter_by(plano_id=current_user.empresa.plano_id, active=True)]

    # Validação
    if form.validate_on_submit():
        telasplano = Telaplano()
        telasplano.alterar_atributos(form)
        db.session.add(telasplano)
        db.session.commit()

        # Mensagens
        if perfil_id > 0:
            flash("Tela atualizada", category="success")

        return redirect(url_for("usuario.viewrole_list", role_id=perfil_id))
    return render_template("viewrole_edit.html", form=form, role_id=perfil_id)


@usuario_blueprint.route('/viewrole_active/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def viewrole_active(perfil_id):
    viewrole = ViewRole.query.filter_by(id=perfil_id).one_or_none()
    if viewrole:
        viewrole.ativar_desativar()
        db.session.add(viewrole)
        db.session.commit()
    return redirect(url_for('usuario.viewrole_list', role_id=viewrole.perfil_id))
