from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.usuario.models import Senha, Usuario, Perfil, Telaperfil
from webapp.contrato.models import Telacontrato
from .forms import LoginForm, AlterarSenhaForm, SolicitarNovaSenhaForm, AlterarSenhaTokenForm, \
    AlterarEmailForm, EditarUsuarioForm, PerfilForm, TelaPerfilForm
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token
from webapp.utils.erros import flash_errors

usuario_blueprint = Blueprint(
    'usuario',
    __name__,
    template_folder='../templates/sistema/usuario',
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
    print(form.nome.data)
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nome=form.nome.data).one_or_none()
        if usuario:
            login_user(usuario)
            return redirect(url_for('sistema.index'))
        else:
            flash("Erro ao logar o usuário no sistema.", category="danger")
    else:
        flash_errors(form)
    return render_template('login.html', form=form)


@usuario_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @usuario_blueprint.route('/<string:nome>/confirm', methods=['GET', 'POST'])
# def resend_confirmation(nome):
#     usuario = Usuario.query.filter_by(nome=nome).one_or_none()
#     token = create_token(usuario.id, usuario.email)
#     send_email(usuario.email,
#                'Confirmação de Conta',
#                'usuario/email/confirm',
#                usuario=usuario,
#                token=token)
#     flash("Um novo email de confirmação foi enviado para o seu email.", category="warning")
#     return redirect(url_for('main.index'))


# alteração de senha quando logado
@usuario_blueprint.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
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
                           'usuario/email/trocar_senha',
                           usuario=current_user)
                flash("Sua senha foi atualizada", category="success")
                return redirect(url_for('main.index'))
            else:
                flash("Senha não atualizada", category="danger")
        else:
            flash("Senha não registrada", category="danger")
    else:
        flash_errors(form)
    return render_template("usuario/trocar_senha.html", form=form)


# solicitação de nova senha
@usuario_blueprint.route('/solicitar_senha', methods=['GET', 'POST'])
def solicitar_senha():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = SolicitarNovaSenhaForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if usuario:
            token = create_token(usuario.id, usuario.email)
            send_email(usuario.email,
                       'Redefinição de Senha',
                       'usuario/email/solicitar_senha',
                       usuario=usuario,
                       token=token)
            flash("Um email com instruções para redefinição de senha foi enviado para seu email.", category="warning")
            return redirect(url_for('usuario.login'))
        else:
            flash("Usuário não cadastrado", category="danger")
    else:
        flash_errors(form)
    return render_template('usuario/solicitar_senha.html', form=form)


# verificar o token antes de solicitar a alteração da senha
@usuario_blueprint.route('/verificar_token_solicitar_senha/<token>', methods=['GET', 'POST'])
def verificar_token_solicitar_senha(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    result, user_id = verify_token("id", token)
    if result:
        usuario = Usuario.query.filter_by(id=user_id).one_or_none()
        if usuario:
            return redirect(url_for('usuario.alterar_senha_token', token=token))
        else:
            flash("Usuário não cadastrado", category="danger")
            return redirect(url_for('main.index'))
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
        return redirect(url_for('main.index'))


# depois de confimado o token libera a tela para alteração de senha
@usuario_blueprint.route('/alterar_senha_token/<token>', methods=['GET', 'POST'])
def alterar_senha_token(token):
    form = AlterarSenhaTokenForm()
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
                               'usuario/email/dados_usuario',
                               usuario=usuario)
                    flash("Sua senha foi atualizada.", category="success")
                    return redirect(url_for('usuario.login'))
                else:
                    flash("Senha não foi alterada", category="danger")
            else:
                flash("Senha não cadastrada", category="danger")
                return redirect(url_for('main.index'))
        else:
            flash_errors(form)
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
        return redirect(url_for('main.index'))
    return render_template('usuario/trocar_senha_token.html', form=form, token=token)


@usuario_blueprint.route('/trocar_email', methods=['GET', 'POST'])
@login_required
def solicitar_troca_email():
    form = AlterarEmailForm()
    token = ""
    if form.validate_on_submit():
        if current_user.verificar_senha(form.senha.data):
            current_user.alterar_email(form.email.data.lower())
            token = create_token(current_user.id, current_user.email)
            send_email(form.email.data.lower(),
                       'Confirme seu novo email',
                       'usuario/email/trocar_email',
                       usuario=current_user,
                       token=token)
            flash("Foi enviado um email com instruções para confirmar seu novo email.", category="warning")
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inválidos", category="danger")
    else:
        flash_errors(form)
    return render_template("usuario/trocar_email.html", form=form, token=token)


@usuario_blueprint.route('/trocar_email/<token>')
@login_required
def trocar_email(token):
    result, email = verify_token("email", token)
    if result:
        usuario = Usuario.query.filter_by(id=current_user.id).one_or_none()
        if usuario:
            usuario.alterar_email(email)
            if usuario.salvar():
                flash("Email atualizado", category="success")
            else:
                flash("Email não atualizado", category="danger")
        else:
            flash("Usuário não cadastrado", category="danger")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@usuario_blueprint.route('/usuario_ativar/<int:usuario_id>')
@login_required
def usuario_ativar(usuario_id):
    """    Função que ativa/inativa um usuário"""
    # retorna o usuário com o identificador
    usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
    if usuario:  # se o usuário existir
        # grava as informações vindas do formulário
        usuario.ativar_desativar()
        # grava as informações no banco de dados
        if usuario.salvar():
            flash("Usuário ativado/desativado", category="success")
        else:
            flash("Usuário não ativado/desativado", category="danger")
    else:  # se o usuário não existir
        flash("Usuário não cadastrado", category="danger")
    return redirect(url_for('usuario.usuario_listar'))


@usuario_blueprint.route('/user/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def usuario(usuario_id):
    usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
    if usuario:
        return render_template('usuario.html', usuario=usuario)
    else:
        flash("Usuário não cadastrado", category="danger")


@usuario_blueprint.route('/usuario_listar', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def usuario_listar() -> str:
    """    Função que retorna uma lista de usuários    """
    # retorna uma lista de usuários da empresa, exceto os adminluz(administradores de sistema)
    usuarios = Usuario.query.filter_by(empresa_id=current_user.empresa_id).\
        filter(Usuario.nome.notlike("%adminluz%")).all()

    return render_template('usuario_listar.html', usuarios=usuarios)


@usuario_blueprint.route('/usuario_editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def usuario_editar(usuario_id):
    """    Função atualiza as informações do usuário    """
    if usuario_id > 0:  # se o identificador foi passado com parâmetro
        # --------- ATUALIZAR
        # instância um usuário com base no identificador
        usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
        # instância um formulário com as informações do usuário
        form = EditarUsuarioForm(obj=usuario)
        new = False  # não é um usuário novo
        form.id.data = usuario_id

        # --------- ATUALIZAR/LER OS DADOS
        if form.perfil.data:
            r_d = form.perfil.data
        else:
            r_d = usuario.perfil_id

    else:
        # --------- CADASTRAR
        usuario = Usuario()  # instância um usuário em branco
        usuario.id = 0
        form = EditarUsuarioForm()  # instância um formulário em branco
        new = True  # é um usuário novo
        r_d = form.perfil.data
        form.id.data = 0

    # --------- LISTAS
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
        usuario.alterar_atributos(form, current_user.empresa_id, new)
        if usuario.salvar():
            if new:
                usuario = Usuario.query.filter_by(nome=form.nome.data).one_or_none()
                # envia o email com as informações de login
                send_email(usuario.email,
                           'Manutenção Luz - Informações para login',
                           'usuario/email/usuario_cadastrado',
                           usuario=usuario)
                flash("Usuário cadastrado", category="success")
            else:
                flash("Usuário atualizado", category="success")
            return redirect(url_for("usuario.usuario_listar"))
        else:
            flash("Usuário não cadastrado/atualizado", category="danger")
            return redirect(url_for("usuario.usuario_editar", usuario_id=usuario_id))
    else:
        flash_errors(form)
    return render_template("usuario_editar.html", form=form, usuario=usuario)


@usuario_blueprint.route('/perfil_listar', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def perfil_listar():
    perfis = Perfil.query.filter_by(empresa_id=current_user.empresa_id).\
        filter(Perfil.nome.notlike("%adminluz%")).all()
    return render_template('perfil_listar.html', perfis=perfis)


@usuario_blueprint.route('/perfil_editar/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def perfil_editar(perfil_id):
    if perfil_id > 0:
        # Atualizar
        perfil = Perfil.query.filter_by(id=perfil_id).first()
        form = PerfilForm(obj=perfil)
        new = False
    else:
        # Cadastrar
        perfil = Perfil()
        perfil.id = 0
        form = PerfilForm()
        new = True

    # Lista
    form.tela.choices = [(telasperfil.id, telasperfil.tela.nome)
                         for telasperfil in Telaperfil.query.filter_by(perfil_id=perfil_id, ativo=True).all()]
    # Validação
    if form.validate_on_submit():
        perfil.alterar_atributos(form, current_user.empresa.id)
        if perfil.salvar():
            if new:
                perfil = Perfil.query.filter_by(nome=form.nome.data, empresa_id=current_user.empresa.id).one_or_none()
                telascontrato = Telacontrato.query.filter_by(contrato_id=current_user.empresa.contrato.id).all()

                for telacontrato in telascontrato:
                    telaperfil = Telaperfil()
                    telaperfil.ativo = False
                    telaperfil.perfil_id = perfil.id
                    telaperfil.tela_id = telacontrato.tela_id
                    if not telaperfil.salvar():
                        flash("Tela do perfil não cadastrado", category="danger")
            # Mensagens
            if perfil_id > 0:
                flash("Perfil atualizado", category="success")
            else:
                flash("Perfil cadastrado", category="success")
            return redirect(url_for("usuario.perfil_listar"))
        else:
            flash("Perfil não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("perfil_editar.html", form=form, perfil=perfil)


@usuario_blueprint.route('/telaperfil_listar/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def telaperfil_listar(perfil_id):
    telasperfil = Telaperfil.query.filter_by(perfil_id=perfil_id).all()
    return render_template('telaperfil_listar.html', telasperfil=telasperfil, perfil_id=perfil_id)


@usuario_blueprint.route('/telaperfil_editar/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def telaperfil_editar(perfil_id):
    form = TelaPerfilForm()

    form.perfil.choices = [(perfis.id, perfis.nome) for perfis in Perfil.query.filter_by(id=perfil_id)]

    form.tela.choices = [(telascontrato.tela.id, telascontrato.tela.nome)
                         for telascontrato in Telacontrato.query.filter_by(contrato_id=current_user.empresa.contrato_id, ativo=True)]

    # Validação
    if form.validate_on_submit():
        telaperfil = Telaperfil()
        telaperfil.alterar_atributos(form)
        if telaperfil.salvar():
            # Mensagens
            if perfil_id > 0:
                flash("Tela do perfil cadastrada", category="success")
            else:
                flash("Tela do perfil atualizada", category="success")
        else:
            flash("Tela do perfil não cadastrada/atualizada", category="success")
        return redirect(url_for("usuario.telaperfil_listar", perfil_id=perfil_id))
    return render_template("telaperfil_editar.html", form=form, perfil_id=perfil_id)


@usuario_blueprint.route('/telaperfil_ativar/<int:perfil_id>', methods=['GET', 'POST'])
@login_required
@has_view('RH')
def telaperfil_ativar(perfil_id):
    telaperfil = Telaperfil.query.filter_by(id=perfil_id).one_or_none()
    if telaperfil:
        telaperfil.ativar_desativar()
        if telaperfil.salvar():
            flash("Tela do perfil ativada/desativada", category="success")
        else:
            flash("Tela do perfil não ativada/desativada", category="danger")
    return redirect(url_for('usuario.telaperfil_listar', perfil_id=telaperfil.perfil_id))
