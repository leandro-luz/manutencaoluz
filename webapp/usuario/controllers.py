import datetime

import numpy as np
import pandas as pd
from flask import (render_template, Blueprint, redirect, url_for, flash, Response)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.usuario.models import Senha, Usuario, PerfilAcesso, TelaPerfilAcesso, PerfilManutentor, \
    PerfilManutentorUsuario
from webapp.empresa.models import Empresa
from webapp.contrato.models import Contrato, Telacontrato, Tela
from .forms import LoginForm, AlterarSenhaForm, SolicitarNovaSenhaForm, AlterarSenhaTokenForm, \
    AlterarEmailForm, EditarUsuarioForm, PerfilAcessoForm, TelaPerfilForm, PerfilManutentorForm
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token
from webapp.utils.erros import flash_errors
from webapp.utils.files import lista_para_csv
from webapp.utils.objetos import salvar_lote, preencher_objeto_atributos_semvinculo, \
    preencher_objeto_atributos_booleanos, preencher_objeto_atributos_datas

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
    if form.validate_on_submit():
        usuario_ = Usuario.query.filter_by(nome=form.nome.data).one_or_none()
        if usuario_:
            login_user(usuario_)
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


# alteração de senha quando logado
@usuario_blueprint.route('/trocar_senha', methods=['GET', 'POST'])
@login_required
def trocar_senha():
    """    Função para alteração de senha de acesso do usuário logado   """

    # verifica se o usuario está ativo
    if not current_user.ativo:
        return redirect(url_for('usuario.logout'))

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
                           'usuario/email/dados_usuario',
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
        usuario_ = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if usuario_:
            token = create_token(usuario_.id, usuario_.email)
            send_email(usuario_.email,
                       'Redefinição de Senha',
                       'usuario/email/solicitar_senha',
                       usuario=usuario_,
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
        usuario_ = Usuario.query.filter_by(id=user_id).one_or_none()
        if usuario_:
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
            usuario_ = Usuario.query.filter_by(id=user_id).one_or_none()
            senha = Senha.query.filter_by(id=user_id).one_or_none()
            if senha:
                senha.alterar_atributos(form)
                if senha.salvar():
                    # enviar email com a senha atualizada
                    send_email(usuario_.email,
                               'Alteração de Senha',
                               'usuario/email/dados_usuario',
                               usuario=usuario_)
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

    # verifica se o usuario está ativo
    if not current_user.ativo:
        return redirect(url_for('usuario.logout'))

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
        usuario_ = Usuario.query.filter_by(id=current_user.id).one_or_none()
        if usuario_:
            usuario_.alterar_email(email)
            if usuario_.salvar():
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
    usuario_ = Usuario.query.filter_by(id=usuario_id).one_or_none()
    if usuario_:  # se o usuário existir
        ativo = usuario_.ativo

        # não permite ativar se o perfilacesso não estivar ativo
        if not ativo:
            if not usuario_.perfilacesso.ativo:
                flash("O perfil de acesso não está ativo", category="danger")
                return redirect(url_for('usuario.usuario_listar'))

        # grava as informações vindas do formulário
        usuario_.ativar_desativar()
        # grava as informações no banco de dados

        if usuario_.salvar():
            if ativo:
                flash("Usuário desativado", category="success")
            else:
                flash("Usuário ativado", category="success")
        else:
            flash("Usuário não ativado/desativado", category="danger")
    else:  # se o usuário não existir
        flash("Usuário não cadastrado", category="danger")
    return redirect(url_for('usuario.usuario_listar'))


@usuario_blueprint.route('/user/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def usuario(usuario_id):
    # verifica se o usuario está ativo
    if not current_user.ativo:
        return redirect(url_for('usuario.logout'))

    usuario_ = Usuario.query.filter_by(id=usuario_id).one_or_none()
    if usuario_:
        return render_template('usuario.html', usuario=usuario_)
    else:
        flash("Usuário não cadastrado", category="danger")


@usuario_blueprint.route('/usuario_listar', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def usuario_listar() -> str:
    """    Função que retorna uma lista de usuários    """
    # retorna uma lista de usuários da empresa, exceto os adminluz(administradores de sistema)
    usuarios = Usuario.query.filter_by(empresa_id=current_user.empresa_id). \
        filter(Usuario.nome.notlike("%adminluz%")).all()

    return render_template('usuario_listar.html', usuarios=usuarios)


@usuario_blueprint.route('/usuario_editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def usuario_editar(usuario_id):
    """    Função atualiza as informações do usuário    """
    if usuario_id > 0:  # se o identificador foi passado com parâmetro
        # --------- ATUALIZAR
        # instância um usuário com base no identificador
        usuario_ = Usuario.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Usuario.empresa_id,
            Usuario.id == usuario_id
        ).one_or_none()

        # verifica se o usuario existe
        if usuario_:
            # instância um formulário com as informações do usuário
            form = EditarUsuarioForm(obj=usuario_)
            new = False  # não é um usuário novo
            form.id.data = usuario_id

            # --------- ATUALIZAR/LER OS DADOS
            if form.perfilacesso.data:
                r_d = form.perfilacesso.data
            else:
                r_d = usuario_.perfilacesso_id

        else:
            flash("Usuário não localizado", category="danger")
            return redirect(url_for("usuario.usuario_listar"))

    else:
        # --------- CADASTRAR
        usuario_ = Usuario()  # instância um usuário em branco
        usuario_.id = 0
        form = EditarUsuarioForm()  # instância um formulário em branco
        new = True  # é um usuário novo
        r_d = form.perfilacesso.data
        form.id.data = 0

    # --------- LISTAS
    form.perfilacesso.choices = [(0, '')] + [(perfis.id, perfis.nome) for perfis in
                                             PerfilAcesso.query.filter_by(empresa_id=current_user.empresa_id).filter(
                                                 PerfilAcesso.nome.notlike("%adminluz%")).all()]
    form.perfilacesso.data = r_d

    permissao_perfil_manutentor = Usuario.verifica_usuario_acesso_tela('Ordem de Serviço')

    form.perfil_manutentor.choices = [(0, '')] + [(pm.id, pm.perfilmanutentor.nome) for pm in
                                                  PerfilManutentorUsuario.query.filter(
                                                      PerfilManutentorUsuario.usuario_id == usuario_id
                                                  ).all()]

    # --------- VALIDAÇÕES
    if form.validate_on_submit():
        # verificar se o perfilacesso está ativo

        if new:
            # instância um novo objeto password_
            password_ = Senha()
            password_.alterar_senha(Senha.senha_aleatoria())
            password_.alterar_data_expiracao()
            password_.salvar()
            usuario_.senha_id = password_.id

        # grava as informações do formulário no objeto usuário
        usuario_.alterar_atributos(form, current_user.empresa_id, new)

        if usuario_.salvar():
            if new:
                usuario_ = Usuario.query.filter_by(nome=form.nome.data).one_or_none()
                # envia o email com as informações de login
                send_email(usuario_.email,
                           'Manutenção Luz - Informações para login',
                           'usuario/email/usuario_cadastrado',
                           usuario=usuario_)
                flash("Usuário cadastrado", category="success")
            else:

                flash("Usuário atualizado", category="success")
            return redirect(url_for("usuario.usuario_listar"))
        else:
            flash("Usuário não cadastrado/atualizado", category="danger")
            return redirect(url_for("usuario.usuario_editar", usuario_id=usuario_id))
    else:
        flash_errors(form)
    return render_template("usuario_editar.html", form=form, usuario=usuario_, ppm=permissao_perfil_manutentor)


@usuario_blueprint.route('/gerar_padrao_usuario/', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def gerar_padrao_usuario():
    # Gera o arquivo csv dos tabela padrão para cadastro em lote
    csv_data = lista_para_csv([[x] for x in Usuario.titulos_doc], None)
    nome = "tabela_base_usuario.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"}
    )


@usuario_blueprint.route('/gerar_csv_usuario/', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def gerar_csv_usuario():
    # Gera o arquivo csv com os titulos
    csv_data = lista_para_csv([[x] for x in Usuario.query.filter_by(empresa_id=current_user.empresa_id)],
                              Usuario.titulos_csv)

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=usuarios.csv'})


@usuario_blueprint.route('/usuario_excluir/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def usuario_excluir(usuario_id):
    usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()

    if usuario:
        if usuario.excluir():
            flash("Usuário excluído", category="success")
        else:
            flash("Erro ao excluir o usuário", category="danger")
    else:
        flash("Usuário não cadastrada", category="danger")
    return redirect(url_for('usuario.usuario_listar'))


@usuario_blueprint.route('/cadastrar_lote_usuarios>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def cadastrar_lote_usuarios():
    form = EditarUsuarioForm()

    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Usuario.titulos_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Usuario.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = Usuario.query.filter_by(empresa_id=current_user.empresa_id).all()

    rejeitados_texto = [['NOME', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos_email = []
    aceitos = []
    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # verifica repetições no BD
        for usuario_ in existentes:
            if usuario_.nome == df.at[linha, 'Nome*']:
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado devido Nome já existir no banco de dados"])
            if usuario_.email == df.at[linha, 'Email*']:
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado devido Email já existir no banco de dados"])

        # verificar existência do perfil
        perfil = PerfilAcesso.query.filter_by(nome=df.at[linha, 'PerfilAcesso*'],
                                              empresa_id=current_user.empresa_id).one_or_none()
        if not perfil:
            rejeitados.append(linha)
            rejeitados_texto.append(
                [df.at[linha, 'Nome*'], "rejeitado devido PerfilAcesso não cadastrado"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Nome*'] in aceitos_cod:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao Nome estar repetido"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Email*'] in aceitos_email:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao Email estar repetido"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # criar uma senha para o usuário
            senha = Senha()
            senha.alterar_senha(Senha.senha_aleatoria())
            senha.alterar_expiravel(True)
            senha.alterar_data_expiracao()
            senha.salvar()

            # preeche os atributos diretamente
            usuario_ = preencher_objeto_atributos_semvinculo(usuario_, usuario_.titulos_doc, df, linha)

            # cria um equipamento e popula ele
            usuario_ = Usuario()

            # dados do usuário
            usuario_.perfilacesso_id = perfil.id
            usuario_.empresa_id = current_user.empresa_id
            usuario_.senha_id = senha.id
            usuario_.data_assinatura = datetime.datetime.now()

            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Nome*'])
            aceitos_email.append(df.at[linha, 'Email*'])
            # insere o equipamento na lista
            aceitos.append(usuario_)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        Usuario.salvar_lote(aceitos)
    flash(f"Total de usuários cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto) - 1}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)

        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=usuarios_rejeitados.csv'})

    return redirect(url_for("usuario.usuario_listar"))


@usuario_blueprint.route('/perfilacesso_listar', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def perfilacesso_listar():
    lista_perfis = [{'perfilacesso': perfilacesso,
                     'total': Usuario.query.filter(Usuario.empresa_id == Empresa.id,
                                                   Usuario.perfilacesso_id == perfilacesso.id,
                                                   Empresa.id == current_user.empresa_id).count(),
                     'telas': TelaPerfilAcesso.query.filter_by(perfilacesso_id=perfilacesso.id).count()}
                    for perfilacesso in PerfilAcesso.query.filter_by(empresa_id=current_user.empresa_id).filter(
            PerfilAcesso.nome.notlike("%adminluz%")).order_by(PerfilAcesso.nome).all()]

    form = PerfilAcessoForm()

    return render_template('perfilacesso_listar.html', perfisacesso=lista_perfis, form=form)


@usuario_blueprint.route('/perfilacesso_editar/<int:perfilacesso_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def perfilacesso_editar(perfilacesso_id):
    usuarios = []
    if perfilacesso_id > 0:
        # Atualizar
        perfilacesso = PerfilAcesso.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == PerfilAcesso.empresa_id,
            PerfilAcesso.id == perfilacesso_id
        ).one_or_none()

        # verifica se o perfil existe
        if perfilacesso:
            form = PerfilAcessoForm(obj=perfilacesso)
            # new = False

            # Usuários vinculados no perfil
            usuarios = Usuario.query.filter_by(perfilacesso_id=perfilacesso.id).all()

        else:
            flash("PerfilAcesso não localizado", category="danger")
            return redirect(url_for("usuario.perfilacesso_listar"))

    else:
        # Cadastrar
        perfilacesso = PerfilAcesso()
        perfilacesso.id = 0
        form = PerfilAcessoForm()
        # new = True

    # LISTA DAS TELAS DO PERFIL ACESSO
    telasperfilacesso_liberadas = TelaPerfilAcesso.query.filter_by(perfilacesso_id=perfilacesso_id).all()

    #  lista(id e nome) de todas as telas liberadas para uso
    telasperfil = Tela.query.filter(
        Tela.id == Telacontrato.tela_id,
        Telacontrato.contrato_id == Contrato.id,
        Contrato.id == Empresa.contrato_id,
        Empresa.id == current_user.empresa_id).order_by(Tela.posicao).all()

    # # Lista de telas já cadastradas
    telasexistentes = Tela.query.filter(
        Tela.id == TelaPerfilAcesso.tela_id,
        TelaPerfilAcesso.perfilacesso_id == perfilacesso_id).order_by(Tela.posicao).all()

    # # Lista de telas permitidas sem repetições
    form_telaperfil = TelaPerfilForm()
    form_telaperfil.tela.choices = [(0, '')] + [(tela.id, tela.nome) for tela in telasperfil if
                                                tela.id not in {tl.id for tl in telasexistentes}]

    # Validação
    if form.validate_on_submit():
        perfilacesso.alterar_atributos(form, current_user.empresa.id)
        if perfilacesso.salvar():
            # Mensagens
            if perfilacesso_id > 0:
                flash("PerfilAcesso atualizado", category="success")
            else:
                flash("PerfilAcesso cadastrado", category="success")
            return redirect(url_for("usuario.perfilacesso_listar"))
        else:
            flash("PerfilAcesso não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("perfilacesso_editar.html", form=form, perfilacesso=perfilacesso, usuarios=usuarios,
                           telasperfilacesso=telasperfilacesso_liberadas, form_telaperfil=form_telaperfil)


@usuario_blueprint.route('/perfilacesso_ativar/<int:perfilacesso_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def perfilacesso_ativar(perfilacesso_id):
    """    Função que ativa/desativa um perfil    """
    # instância um perfil com base no identificador
    perfilacesso = PerfilAcesso.query.filter_by(id=perfilacesso_id).one_or_none()
    # se o perfil existir
    if perfilacesso:
        ativo = perfilacesso.ativo

        if not ativo:
            # realiza a contagem de telas ativas para este perfil
            # se for zero não permite a ativação
            if TelaPerfilAcesso.contagem_telas_ativas(perfilacesso_id) == 0:
                flash("Não permitido ativar perfil sem nenhuma tela ativa neste perfil", category="danger")
                return redirect(url_for('usuario.perfilacesso_listar'))

        # ativa/inativa o perfil
        perfilacesso.ativar_desativar()
        # salva no banco de dados a alteração
        if perfilacesso.salvar():
            if ativo:
                # Busca os usuarios vinculados ao perfilacesso e inativa eles
                Usuario.inativar_by_perfilacesso(perfilacesso_id)

                flash("Perfil de Acesso desativado com sucesso", category="success")
            else:
                flash("Perfil de Acesso ativado com sucesso", category="success")
        else:
            flash("PerfilAcesso não foi ativado/desativado", category="danger")
    else:
        flash("PerfilAcesso não registrado", category="danger")
    return redirect(url_for('usuario.perfilacesso_listar'))


@usuario_blueprint.route('/gerar_padrao_perfis/', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def gerar_padrao_perfis():
    csv_data = lista_para_csv([[x] for x in PerfilAcesso.titulos_doc], None)
    nome = "tabela_base_perfis.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"}
    )


@usuario_blueprint.route('/perfilacesso_excluir/<int:perfilacesso_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def perfilacesso_excluir(perfilacesso_id):
    perfilacesso = PerfilAcesso.query.filter_by(id=perfilacesso_id).one_or_none()

    if perfilacesso:
        if perfilacesso.excluir():
            flash("Perfil de Acesso excluído", category="success")
        else:
            flash("Erro ao excluir o perfil de acesso", category="danger")
    else:
        flash("Perfil de acesso não cadastrado", category="danger")
    return redirect(url_for('usuario.perfilacesso_listar'))


@usuario_blueprint.route('/cadastrar_lote_perfis/>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def cadastrar_lote_perfis():
    form = PerfilAcessoForm()

    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=PerfilAcesso.titulos_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in PerfilAcesso.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.nome for x in PerfilAcesso.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == PerfilAcesso.empresa_id
    ).all()]

    rejeitados_texto = [['NOME', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []
    ativos = ['SIM', 'OK', 'POSITIVO', 'VERDADEIRO', 1, '1', 'TRUE', True, 'Ativo']

    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        ativo = False
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        if df.at[linha, 'Nome*'] in titulos_obrigatorio:
            # rejeitado provavelmente é o título
            rejeitados.append(linha)

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Nome*'] in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado por já existir no banco de dados"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Nome*'] in aceitos_cod:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido a estar repetido"])

        # verifica o valor do campo ativo
        if df.at[linha, 'Ativo'] is not None:
            if df.at[linha, 'Ativo'] in ativos:
                ativo = True

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # cria um equipamento e popula ele
            perfil = PerfilAcesso()
            perfil.nome = df.at[linha, 'Nome*']
            perfil.descricao = df.at[linha, 'Descrição']
            perfil.ativo = ativo
            perfil.empresa_id = current_user.empresa_id
            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Nome*'])
            # insere o equipamento na lista
            aceitos.append(perfil)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        for aceito in aceitos:
            aceito.salvar()

    flash(f"Total de perfis cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto) - 1}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 1:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)

        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=perfis_rejeitados.csv'})

    return redirect(url_for('usuario.perfil_listar'))


@usuario_blueprint.route('/telaperfilacesso_listar/<int:perfilacesso_id>>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def telaperfilacesso_listar(perfilacesso_id):
    telasperfilacesso_liberadas = TelaPerfilAcesso.query.filter_by(perfilacesso_id=perfilacesso_id).all()

    #  lista(id e nome) de todas as telas liberadas para uso
    telasperfil = Tela.query.filter(
        Tela.id == Telacontrato.tela_id,
        Telacontrato.contrato_id == Contrato.id,
        Contrato.id == Empresa.contrato_id,
        Empresa.id == current_user.empresa_id).order_by(Tela.posicao)

    # # Lista de telas já cadastradas
    telasexistentes = Tela.query.filter(
        Tela.id == TelaPerfilAcesso.tela_id,
        TelaPerfilAcesso.perfilacesso_id == perfilacesso_id).order_by(Tela.posicao)

    # # Lista de telas permitidas sem repetições
    form = TelaPerfilForm()
    form.tela.choices = [(tela.id, tela.nome) for tela in telasperfil if
                         tela.id not in {tl.id for tl in telasexistentes}]

    return render_template('telaperfilacesso_listar.html', telasperfilacesso=telasperfilacesso_liberadas,
                           perfilacesso_id=perfilacesso_id, form=form)


@usuario_blueprint.route('/telaperfilacesso_editar/<int:perfilacesso_id>>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def telaperfilacesso_editar(perfilacesso_id):
    perfilacesso = PerfilAcesso.query.filter_by(id=perfilacesso_id).one_or_none()
    form = TelaPerfilForm()

    if perfilacesso:
        if form.validate_on_submit():
            telaperfilacesso = TelaPerfilAcesso()
            telaperfilacesso.alterar_atributos(form, perfilacesso_id)
            if telaperfilacesso.salvar():
                flash("Tela do perfil cadastrada", category="success")
            else:
                flash("Erro ao cadastrar perfil", category="danger")
        else:
            flash_errors(form)
    else:
        flash("Perfil não cadastrado", category="danger")

    return redirect(url_for("usuario.perfilacesso_editar", perfilacesso_id=perfilacesso_id))


@usuario_blueprint.route('/telaperfilacesso_excluir/<int:telaperfilacesso_id>/<int:perfilacesso_id>',
                         methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
def telaperfilacesso_excluir(telaperfilacesso_id, perfilacesso_id):
    # verifica se a telaperfilacesso existe
    telaperfilacesso = TelaPerfilAcesso.query.filter_by(id=telaperfilacesso_id).one_or_none()
    if telaperfilacesso:
        # realiza a exclusão da telaperfilacesso
        if telaperfilacesso.excluir():
            # quando desativar, verifica os usuarios vinculados, se existir
            TelaPerfilAcesso.verifica_usuarios_vinculados(perfilacesso_id)
            flash("Tela do perfil desativada", category="success")
        else:
            flash("Tela do perfil não ativada/desativada", category="danger")
    return redirect(url_for('usuario.perfilacesso_editar', perfilacesso_id=perfilacesso_id))


@usuario_blueprint.route('/perfilmanutentor_listar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
@has_view('Ordem de Serviço')
def perfilmanutentor_listar(usuario_id):
    if usuario_id == 0:
        flash("Usuário não cadastrado", category="danger")
        return redirect(url_for('usuario.usuario_editar', usuario_id=usuario_id))
    else:
        perfismanutentor_existentes = PerfilManutentorUsuario.query.filter_by(usuario_id=usuario_id).all()
        perfis = PerfilManutentor.query.all()

        # # Lista de telas permitidas sem repetições
        form = PerfilManutentorForm()
        form.perfilmanutentor.choices = [(0, '')] + [(perfil.id, perfil.nome) for perfil in perfis if
                                                     perfil.id not in {pm.perfilmanutentor.id for pm in
                                                                       perfismanutentor_existentes}]

    return render_template("perfilmanutentor_listar.html", perfismanutentor=perfismanutentor_existentes,
                           usuario_id=usuario_id, form=form)


@usuario_blueprint.route('/perfilmanutentor_editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
@has_view('Usuário')
@has_view('Ordem de Serviço')
def perfilmanutentor_editar(usuario_id):
    usuario_ = Usuario.query.filter_by(id=usuario_id).one_or_none()
    form = PerfilManutentorForm()

    # verifica se o usuário está cadastrado
    if not usuario_:
        flash("Usuário não cadastrado", category="danger")
        return redirect(url_for('usuario.usuario_editar', usuario_id=usuario_id))
    else:
        # pesquisa os perfis manutentor cadastrado
        form.perfilmanutentor.choices = [(0, '')] + [(pm.id, pm.nome)
                                                     for pm in PerfilManutentor.query.all()]
        form.usuario_id.data = usuario_.id

    # Realiza a validação do formulário
    if form.validate_on_submit():
        perfilmanutentorusuario = PerfilManutentorUsuario()
        perfilmanutentorusuario.alterar_atributos(form, usuario_id)
        if perfilmanutentorusuario.salvar():
            flash("Perfil Manutentor Cadastrado", category="success")
        else:
            flash("Perfil Manutentor não Cadastrado", category="danger")
        return redirect(url_for('usuario.perfilmanutentor_listar', usuario_id=usuario_id))
    else:
        flash_errors(form)

    return redirect(url_for('usuario.perfilmanutentor_listar', usuario_id=usuario_id))


@usuario_blueprint.route('/perfilmanutentor_excluir/<int:usuario_id>/<int:perfilmanutentorusuario_id>')
@login_required
@has_view('Usuário')
@has_view('Ordem de Serviço')
def perfilmanutentor_excluir(usuario_id, perfilmanutentorusuario_id):
    # retorna o usuário com o identificador
    usuario_ = Usuario.query.filter_by(id=usuario_id).one_or_none()
    if usuario_:
        # Busca o perfil, e verifica se o mesmo existe
        perfilmanutentorusuario = PerfilManutentorUsuario.query.filter_by(id=perfilmanutentorusuario_id).one_or_none()
        if perfilmanutentorusuario:

            # grava as informações no banco de dados
            if perfilmanutentorusuario.excluir():
                flash("Perfil manutentor excluir", category="success")
            else:
                flash("Erro ao excluir o perfil manutentoro", category="danger")
        else:
            flash("Perfil não cadastrado para este usuário", category="danger")

    else:  # se o usuário não existir
        flash("Usuário não cadastrado", category="danger")

    return redirect(url_for('usuario.perfilmanutentor_listar', usuario_id=usuario_id))
