import config
from flask import (render_template, Blueprint,
                   redirect, url_for,
                   flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.empresa.forms import EmpresaForm, EmpresaSimplesForm, RegistroInteressadoForm
from webapp.contrato.models import Contrato
from webapp.usuario.models import Senha, Usuario, Perfil, Telaperfil
from webapp.contrato.models import Telacontrato
from webapp.equipamento.models import Grupo
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token
from webapp.utils.erros import flash_errors

empresa_blueprint = Blueprint(
    'empresa',
    __name__,
    template_folder='../templates/sistema/empresa',
    url_prefix="/sistema"
)


@empresa_blueprint.route('/empresa_listar', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_listar() -> str:
    """    Retorna a lista de empresas vinculada a empresa do usuario     """
    empresas = Empresa.query.filter_by(empresa_gestora_id=current_user.empresa_id)  # retorna uma lista com base no _
    # identificador da empresa do usuário
    return render_template('empresa_listar.html', empresas=empresas)


@empresa_blueprint.route('/empresa_ativar/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_ativar(empresa_id):
    """    Função que ativa/desativa uma empresa    """
    empresa = Empresa.query.filter_by(id=empresa_id).one_or_none()  # instância uma empresa com base no identificador
    if empresa:  # se a empresa existir
        empresa.ativar_desativar()  # ativa/inativa a empresa
        if empresa.salvar():  # salva no banco de dados a alteração
            flash("Empresa ativada/desativada com sucesso", category="success")
        else:
            flash("Empresa não foi ativada/desativada", category="danger")
    else:
        flash("Empresa não registrada", category="danger")
    return redirect(url_for('empresa.empresa_listar'))


@empresa_blueprint.route('/empresa_editar/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_editar(empresa_id):
    """   Função que altera os valores    """
    if empresa_id > 0:  # se o identificador foi passado como parâmetro
        # --------- LER
        # instância uma empresa com base no idenfificador
        empresa = Empresa.query.filter_by(id=empresa_id).first()
        form = EmpresaForm(obj=empresa)  # instânciar o formulário
        new = False  # não é uma empresa nova

        # instância um contrato de assinatura com base no identificador do contrato da empres
        contrato = Contrato.query.filter_by(id=empresa.contrato_id).one_or_none()

        # --------- ATUALIZAR
        if form.contrato.data:  # se os dados já foram preenchidos
            p_d = form.contrato.data
        else:  # pegar os dados selecionados
            p_d = contrato.id
    else:
        # --------- CADASTRAR
        empresa = Empresa()  # instânciar o objeto empresa
        empresa.id = 0  # informar o id como 0
        form = EmpresaForm()  # instânciar o formulário para empresa
        new = True  # é uma empresa nova
        p_d = form.contrato.data

    # --------- LISTAS
    form.contrato.choices = [(plans.id, plans.nome) for plans in Contrato.query.all()]
    form.contrato.data = p_d

    # atribuindo o tipo "Cliente" para a empresa
    tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():
        empresa.alterar_atributos(form, current_user.empresa_id, tipoempresa.id, new)
        if empresa.salvar():
            if new:
                empresa = Empresa.query.filter_by(nome_fantasia=form.nome_fantasia.data).one_or_none()
                new_admin(empresa)
            # --------- MENSAGENS
            if empresa_id > 0:
                flash("Empresa atualizada", category="success")
            else:
                flash("Empresa cadastrada, informações enviado ao email", category="success")

            return redirect(url_for("empresa.empresa_listar"))
        else:
            flash("Erro ao salvar a empresa", category="danger")
    else:
        flash_errors(form)
    return render_template("empresa_editar.html", form=form, empresa=empresa)


def new_admin(empresa: [Empresa]):
    """    Função para cadastrar os (administradores, grupos) da empresa    """

    # salvar um modelo de grupo vazio para os equipamentos da empresa
    grupo = Grupo()
    grupo.nome = 'None'
    grupo.empresa_id = empresa.id
    if not grupo.salvar():
        flash("Erro ao cadastrar o grupo de ativos", category="danger")

    # lista dos administradores
    lista = [{'nome': 'admin', 'descricao': 'administrador',
              'email': empresa.email, 'senha_temporaria': True},
             {'nome': 'adminluz', 'descricao': 'administrador do sistema',
              'email': config.Config.MAIL_USERNAME, 'senha_temporaria': False},
             ]

    # laço de repetição
    for valor in lista:
        # cadastro da regra
        perfil = Perfil(nome=valor['nome'], descricao=valor['descricao'], empresa_id=empresa.id)
        if not perfil.salvar():
            flash("Erro ao salvar o perfil", category="danger")
            break

        # busca a lista de telas liberadas para a empresa
        telascontrato = Telacontrato.query.filter_by(contrato_id=empresa.contrato_id).all()
        for telacontrato in telascontrato:
            # cadastro de viewroles para o administrador
            telaperfil = Telaperfil(perfil_id=perfil.id, tela_id=telacontrato.tela_id, ativo=telacontrato.ativo)
            if not telaperfil.salvar():
                flash("Erro ao salvar a tela no perfil", category="danger")
                break

        # instância um novo objeto password_
        senha = Senha()
        if valor['senha_temporaria']:
            # informa a senha de administrador do sistema, a senha não expira
            senha.alterar_senha(Senha.senha_aleatoria())
            senha.alterar_expiravel(False)
        else:
            # informa uma senha temporária para o administrador da empresa, e informa a data de expiração da senha
            senha.alterar_senha(Senha.password_adminluz())
            senha.alterar_data_expiracao()
            senha.alterar_senha_temporaria(False)
        if not senha.salvar():
            flash("Erro ao salvar a senha do usuário", category="danger")
            break

        # instância um novo objeto usuário
        usuario = Usuario()
        # cria os usuários administradores do sistema para a nova empresa
        usuario.usuario_administrador(nome=valor['nome'] + "_" + empresa.nome_fantasia,
                                      email=valor['email'], empresa_id=empresa.id,
                                      perfil_id=perfil.id, senha_id=senha.id)

        if usuario.salvar():
            # envia o email com as informações de login

            if not send_email(valor['email'],
                              'Manutenção Luz - Informações para login',
                              'usuario/email/usuario_cadastrado',
                              usuario=usuario):
                flash("Erro ao cadastrar o usuário administrador para esta empresa", category="danger")
                break
        else:
            flash("Usuário administrador não cadastrado", category="danger")
            break


@empresa_blueprint.route('/solicitar', methods=['GET', 'POST'])
def solicitar():
    form = RegistroInteressadoForm()
    if form.validate_on_submit():
        interessado = Interessado()
        interessado.alterar_atributos(form)
        if interessado.salvar():
            flash("Informações enviadas com sucesso, em breve vamos lhe atender", category="success")
        else:
            flash("Interessado não registrado", category="danger")
        return redirect(url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('interessado_solicitar.html', form=form)


@empresa_blueprint.route('/interessado_listar', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def interessado_listar() -> str:
    """    Função que retorna uma lista com interessados     """
    # retorna uma lista de interessados
    interessados = Interessado.query.order_by(Interessado.data_solicitacao.desc())
    return render_template('interessado_listar.html', interessados=interessados)


@empresa_blueprint.route('/enviar_link/<int:interessado_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def enviar_link(interessado_id):
    interessado = Interessado.query.filter_by(id=interessado_id).one_or_none()
    if interessado:
        token = create_token(interessado.id, interessado.email)
        if send_email(interessado.email,
                      'Solicitação de acesso',
                      'empresa/email/proposta',
                      interessado=interessado,
                      token=token):
            flash(f'Foi enviado para o email as propostas de cadastro para a empresa {interessado.nome_fantasia}',
                  category="success")
        else:
            flash("Erro ao enviar o link para o interessado", category="danger")
    else:
        flash("Interessado não cadastrado", category="danger")
    return redirect(url_for('empresa.interessado_listar'))


@empresa_blueprint.route('/interessado_confirmar/<token>', methods=['GET', 'POST'])
def interessado_confirmar(token):
    """    Função de confirmação do token do lead    """
    # consulta as informações do token enviado
    result, interessado_id = verify_token("id", token)
    # se o token está válido
    if result:
        # instância um novo lead
        interessado = Interessado.query.filter_by(id=interessado_id).one_or_none()
        # cria um novo token de segurança
        token = create_token(interessado.id, interessado.email)
        # cria uma empresa e importa as informações do lead
        empresa = Empresa()
        empresa.importar_interessado(interessado)
        # instânciar o formulário com as informações inicias do interessado
        form = EmpresaSimplesForm(obj=empresa)
        # --------- LISTAS
        form.contrato.choices = [(plans.id, plans.nome) for plans in Contrato.query.all()]

        # redireciona para a tela de registro de empresa, usando token
        return render_template('empresa_registrar.html', form=form, token=token)
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@empresa_blueprint.route('/empresa_registrar/<token>', methods=['GET', 'POST'])
def empresa_registrar(token):
    """    Função que grava as informações de um cadastro empresa externo    """
    # consulta as informações do token enviado
    result, interessado_id = verify_token("id", token)
    form = EmpresaSimplesForm()
    # se o token está válido
    if result:
        if form.validate_on_submit():
            new = True
            empresa = Empresa()
            # buscando a empresa gestora principal
            gestora = Empresa.query.filter_by(nome_fantasia='empresa_1').one_or_none()
            # atribuindo o tipo "Cliente" para a empresa
            tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()

            empresa.alterar_atributos_externo(form, gestora.id, tipoempresa.id, new)

            if empresa.salvar():
                # instância um lead
                interessado = Interessado.query.filter_by(id=interessado_id).one_or_none()
                # registra o lead como cadastrado
                interessado.registrado()
                # criar os admnistradores para a empresa
                new_admin(empresa)
                flash("Empresa registrada, informações de acesso enviadas ao email", category="success")
                return redirect(url_for('usuario.login'))
                # else:
                #     flash("Erro ao cadastrar o usuário do sistema", category="danger")
                #     return redirect(url_for('main.index'))
            else:
                flash("Empresa não registrada", category="danger")
        else:
            flash_errors(form)
            # flash("O cadastro não foi realizado", category="danger")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))
