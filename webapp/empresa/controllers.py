import config
from flask import (render_template, Blueprint,
                   redirect, jsonify, url_for,
                   flash)
from flask_login import current_user, login_required
from webapp.empresa.models import db, Interessado, Tipoempresa, Empresa, Business, Subbusiness
from webapp.empresa.forms import EmpresaForm, BusinessForm, SubbusinessForm, RegistroEmpresaForm
from webapp.plano.models import Plano
from webapp.usuario.models import Senha, Usuario, Perfil, ViewRole
from webapp.plano.models import Telaplano
from webapp.equipamento.models import Grupo
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token

empresa_blueprint = Blueprint(
    'empresa',
    __name__,
    template_folder='../templates/sistema/empresa',
    url_prefix="/sistema"
)


@empresa_blueprint.route('/company_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_list() -> str:
    """    Retorna a lista de empresas vinculada a empresa do usuario     """
    empresas = Empresa.query.filter_by(empresa_gestora_id=current_user.empresa_id)  # retorna uma lista com base no _
    # identificador da empresa do usuário
    return render_template('company_list.html', empresas=empresas)


@empresa_blueprint.route('/empresa/subbusiness_list_option/<int:business_id>', methods=['GET', 'POST'])
@login_required
def subbusiness_list_option(business_id: int):
    """    Função que retorna lista de subnegócios"""
    subbusinesslist = Subbusiness.query.filter_by(business_id=business_id).all()  # retorna uma lista de subnegócios _
    # com base no identificador
    subbusinessarray = []
    for subbusiness in subbusinesslist:
        subbusinessobj = {'id': subbusiness.id, 'nome': subbusiness.nome}
        subbusinessarray.append(subbusinessobj)
    return jsonify({'subbusiness_list': subbusinessarray})


@empresa_blueprint.route('/company_active/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_active(empresa_id):
    """    Função que ativa/desativa uma empresa    """
    empresa = Empresa.query.filter_by(id=empresa_id).one_or_none()  # instância uma empresa com base no identificador
    if empresa:  # se a empresa existir
        empresa.ativar_desativar()  # ativa/inativa a empresa
        empresa.salvar()  # salva no banco de dados a alteração
    else:
        flash("Empresa não registrada", category="danger")
    return redirect(url_for('empresa.company_list'))


@empresa_blueprint.route('/company_edit/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def company_edit(empresa_id):
    """   Função que altera os valores    """
    if empresa_id > 0:  # se o identificador foi passado como parâmetro
        # --------- LER
        # instância uma empresa com base no idenfificador
        empresa = Empresa.query.filter_by(id=empresa_id).first()
        form = EmpresaForm(obj=empresa)  # instânciar o formulário
        new = False  # não é uma empresa nova

        # buscar os subnegócios da empresa
        subbusiness = Subbusiness.query.filter_by(id=empresa.subbusiness_id).one_or_none()

        # instância um plano de assinatura com base no identificador do plano da empres
        plan = Plano.query.filter_by(id=empresa.plano_id).one_or_none()

        # --------- ATUALIZAR
        if form.business.data:  # se os dados já foram preenchidos
            b_d = form.business.data
            sb_d = form.subbusiness.data
            p_d = form.plano.data
        else:  # pegar os dados selecionados
            b_d = subbusiness.business_id
            sb_d = subbusiness.id
            p_d = plan.id
    else:
        # --------- CADASTRAR
        empresa = Empresa()  # instânciar o objeto empresa
        empresa.id = 0  # informar o id como 0
        form = EmpresaForm()  # instânciar o formulário para empresa
        new = True  # é uma empresa nova
        b_d = 1
        subbusiness = Subbusiness.query.filter_by(business_id=b_d).first()
        sb_d = subbusiness.id
        p_d = form.plano.data

    # --------- LISTAS
    form.business.choices = [(business.id, business.nome) for business in Business.query.all()]
    form.business.data = b_d

    form.subbusiness.choices = [(subbusiness.id, subbusiness.nome)
                                for subbusiness in Subbusiness.query.filter_by(business_id=b_d)]
    form.subbusiness.data = sb_d

    form.plano.choices = [(plans.id, plans.nome) for plans in Plano.query.all()]
    form.plano.data = p_d

    # atribuindo o tipo "Cliente" para a empresa
    tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()
    empresa.companytype_id = tipoempresa.id

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():
        empresa.alterar_atributos(form, current_user.empresa_id, new)
        empresa.salvar()

        if new:
            empresa = Empresa.query.filter_by(razao_social=form.razao_social.data).one_or_none()
            new_admin(empresa)
            flash("Usuário cadastrado com sucesso, informações de acesso enviadas ao email", category="success")
            # else:
            #     flash("Erro ao cadastrar o usuário do sistema", category="danger")
        # --------- MENSAGENS
        if empresa_id > 0:
            flash("Empresa atualizada", category="success")
        else:
            flash("Empresa cadastrada", category="success")

        return redirect(url_for("empresa.company_list"))
    return render_template("company_edit.html", form=form, empresa=empresa)


def new_admin(empresa: [Empresa]):
    """    Função para cadastrar os (administradores, grupos) da empresa    """

    # salvar um modelo de grupo vazio para os equipamentos da empresa
    group = Grupo()
    group.nome= 'None'
    group.empresa_id = empresa.id
    group.salvar()

    # lista dos administradores
    lista = [{'nome': 'admin_', 'email': empresa.email, 'senha_temporaria': True},
             {'nome': 'adminluz_', 'email': config.Config.MAIL_USERNAME, 'senha_temporaria': False},
             ]
    # laço de repetição
    for valor in lista:
        # cadastro da regra
        role = Perfil(nome='admin', descricao='administrador', empresa_id=empresa.id)
        role.salvar()

        # busca a lista de telas liberadas para a empresa
        viewplans = Telaplano.query.filter_by(plano_id=empresa.plano_id).all()
        for viewplan in viewplans:
            # cadastro de viewroles para o administrador
            viewrole = ViewRole(role_id=role.id, tela_id=viewplan.tela_id, active=viewplan.ativo)
            viewrole.salvar()

        # instância um novo objeto password_
        password_ = Senha()
        if valor['senha_temporaria']:
            # informa a senha de administrador do sistema, a senha não expira
            password_.alterar_senha(Senha.senha_aleatoria())
            password_.alterar_expiravel(False)
        else:
            # informa uma senha temporária para o administrador da empresa, e informa a data de expiração da senha
            password_.alterar_senha(Senha.password_adminluz())
            password_.alterar_data_expiracao()
            password_.alterar_senha_temporaria(False)
        password_.salvar()

        # instância um novo objeto usuário
        user = Usuario()
        # cria os usuários administradores do sistema para a nova empresa
        user.usuario_administrador(nome=valor['nome'] + empresa.razao_social, email=valor['email'], empresa_id=empresa.id,
                                   role_id=role.id, password_=password_.id)

        if user.save():
            # envia o email com as informações de login
            send_email(valor['email'],
                       'Manutenção Luz - Informações para login',
                       'auth/email/confirm',
                       user=user)


@empresa_blueprint.route('/business_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def business_list() -> str:
    """    Função que retorna uma lista de negócios    """
    businesss = Business.query.order_by(Business.nome.asc())
    return render_template('business_list.html', businesss=businesss)


@empresa_blueprint.route('/business/<int:business_id>', methods=['GET', 'POST'])
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

        return redirect(url_for("empresa.business_list"))
    return render_template("business_edit.html", form=form, business=business)


@empresa_blueprint.route('/subbusiness_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def subbusiness_list() -> str:
    """    Função que retorna uma lista com subnegócios     """
    # retorna uma lista de subnegócios
    subbusinesss = Subbusiness.query.order_by(Subbusiness.business_id.asc())
    return render_template('subbusiness_list.html', subbusinesss=subbusinesss)


@empresa_blueprint.route('/subbusiness/<int:subbusiness_id>', methods=['GET', 'POST'])
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
    form.business.choices = [(business.id, business.nome) for business in Business.query.all()]
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

        return redirect(url_for("empresa.subbusiness_list"))
    return render_template("subbusiness_edit.html", form=form, subbusiness=subbusiness)


@empresa_blueprint.route('/request', methods=['GET', 'POST'])
def request():
    form = RegistroEmpresaForm()
    if form.validate_on_submit():
        interessado = Interessado()
        interessado.alterar_atributos(form)
        if interessado.save():
            flash("Informações enviadas com sucesso, em breve vamos lhe atender", category="success")

        return redirect(url_for('main.index'))
    return render_template('company_request.html', form=form)


@empresa_blueprint.route('/lead_list', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def lead_list() -> str:
    """    Função que retorna uma lista com interessados     """
    # retorna uma lista de interessados
    interessados = Interessado.query.order_by(Interessado.data_solicitacao.desc())
    return render_template('lead_list.html', interessados=interessados)


@empresa_blueprint.route('/enviar_link/<int:interessado_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def enviar_link(interessado_id):
    interessado = Interessado.query.filter_by(id=interessado_id).first()
    try:
        token = create_token(interessado.id, interessado.email)
        send_email(interessado.email,
                   'Solicitação de acesso',
                   'empresa/email/proposta',
                   interessado=interessado,
                   token=token)
        flash(f'Foi enviado para o email as propostas de cadastro para a empresa {interessado.razao_social}', category="success")
    except:
        flash("Erro ao enviar o link para o interessado", category="danger")
    return redirect(url_for('empresa.lead_list'))


@empresa_blueprint.route('/lead_confirm/<token>', methods=['GET', 'POST'])
def lead_confirm(token):
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
        form = EmpresaForm(obj=empresa)
        # --------- LISTAS
        form.business.choices = [(business.id, business.nome) for business in Business.query.all()]
        form.subbusiness.choices = [(subbusiness.id, subbusiness.nome)
                                    for subbusiness in Subbusiness.query.filter_by(business_id=1)]
        form.plano.choices = [(plans.id, plans.nome) for plans in Plano.query.all()]

        # redireciona para a tela de registro de empresa, usando token
        return render_template('company_register.html', form=form, token=token)
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))


@empresa_blueprint.route('/company_register/<token>', methods=['GET', 'POST'])
def company_register(token):
    """    Função que grava as informações de um cadastro empresa externo    """
    # consulta as informações do token enviado
    result, interessado_id = verify_token("id", token)
    form = EmpresaForm()
    # se o token está válido
    if result:
        if form.validate_on_submit():
            new = True
            empresa = Empresa()
            empresa.alterar_atributos_externo(form, 1, new)
            # atribuindo o tipo "Cliente" para a empresa
            tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()
            empresa.tipoempresa_id = tipoempresa.id

            if empresa.salvar():
                # instância um lead
                interessado = Interessado.query.filter_by(id=interessado_id).one_or_none()
                # registra o lead como cadastrado
                interessado.registrado()
                # criar os admnistradores para a empresa
                new_admin(empresa)
                flash("Usuário cadastrado com sucesso, informações de acesso enviadas ao email", category="success")
                return redirect(url_for('usuario.login'))
                # else:
                #     flash("Erro ao cadastrar o usuário do sistema", category="danger")
                #     return redirect(url_for('main.index'))
        else:
            flash("O cadastro não foi realizado", category="danger")
    else:
        flash("O link para confirmação é invalido ou está expirado!", category="danger")
    return redirect(url_for('main.index'))
