import config
from flask import (render_template, Blueprint,
                   redirect, url_for,
                   flash)
from flask_login import current_user, login_required, login_user
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.empresa.forms import EmpresaForm, EmpresaSimplesForm, RegistroInteressadoForm
from webapp.contrato.models import Contrato
from webapp.usuario.models import Senha, Usuario, PerfilAcesso, TelaPerfilAcesso
from webapp.usuario.forms import LoginForm
from webapp.contrato.models import Telacontrato
from webapp.usuario import has_view
from webapp.utils.email import send_email
from webapp.utils.tools import create_token, verify_token
from webapp.utils.erros import flash_errors
from webapp.utils.files import arquivo_padrao
import pandas as pd
import numpy as np

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

    return render_template('empresa_listar.html', empresas=empresas)


@empresa_blueprint.route('/empresa_cliente', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_cliente() -> str:
    """    Retorna a lista de empresas vinculada a empresa do usuario     """
    empresa = Empresa.query.filter_by(id=1).one_or_none()
    empresas = {empresa.nome_fantasia: lista_clientes(current_user.empresa_id)}

    return render_template('empresa_cliente.html', empresas=empresas)


def lista_clientes(id):
    clientes = Empresa.query.filter(
        Empresa.id != 1,
        Empresa.empresa_gestora_id == id).all()

    return [{cliente.nome_fantasia: lista_clientes(cliente.id)} for cliente in clientes]


@empresa_blueprint.route('/empresa_ativar/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_ativar(empresa_id):
    """    Função que ativa/desativa uma empresa    """
    empresa = Empresa.query.filter_by(id=empresa_id).one_or_none()  # instância uma empresa com base no identificador
    if empresa:  # se a empresa existir
        ativo = empresa.ativo

        # caso a empresa não esteja ativa
        if not ativo:
            # caso o contrato não esteja ativo
            if not empresa.contrato.ativo:
                flash("O contrato desta empresa não está ativo", category="danger")
                return redirect(url_for('empresa.empresa_listar'))

        empresa.ativar_desativar()  # ativa/inativa a empresa
        if empresa.salvar():  # salva no banco de dados a alteração
            if ativo:
                flash("Empresa desativada com sucesso", category="success")
            else:
                flash("Empresa ativada com sucesso", category="success")
        else:
            flash("Erro ao ativar/desativar empresa", category="danger")

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
        # localiza a empresa
        empresa = Empresa.query.filter(
            Empresa.id == empresa_id,
            Empresa.empresa_gestora_id == current_user.empresa_id
        ).one_or_none()

        # se empresa existir
        if empresa:
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
            flash("Empresa não localizada", category="danger")
            return redirect(url_for('empresa.empresa_listar'))
    else:
        # --------- CADASTRAR
        empresa = Empresa()  # instânciar o objeto empresa
        empresa.id = 0  # informar o id como 0
        form = EmpresaForm()  # instânciar o formulário para empresa
        new = True  # é uma empresa nova
        p_d = form.contrato.data

    # --------- LISTAS
    form.contrato.choices = [(0, '')] + [(contratos.id, contratos.nome)
                                         for contratos in Contrato.query.filter(
            Contrato.ativo == True,
            Contrato.empresa_gestora_id == current_user.empresa_id).all()]
    form.contrato.data = p_d

    # atribuindo o tipo "Cliente" para a empresa
    tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():
        empresa.alterar_atributos(form, current_user.empresa_id, tipoempresa.id, new)
        if empresa.salvar():
            if new:
                empresa = Empresa.query.filter(Empresa.cnpj == form.cnpj.data,
                                               Empresa.empresa_gestora_id == current_user.empresa_id).one_or_none()
                new_admin(empresa, form.enviar_email.data)
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


def new_admin(empresa: [Empresa], enviar_email):
    """    Função para cadastrar os (administradores, grupos) da empresa    """

    # lista dos administradores
    lista = [{'nome': 'admin', 'descricao': 'administrador',
              'email': empresa.email, 'enviar_email': True, 'senha_temporaria': True},
             {'nome': 'adminluz', 'descricao': 'administrador do sistema',
              'email': config.Config.MAIL_USERNAME, 'enviar_email': False, 'senha_temporaria': False},
             ]

    # laço de repetição
    for valor in lista:
        # cadastro da regra
        perfilacesso = PerfilAcesso(nome=valor['nome'], descricao=valor['descricao'], empresa_id=empresa.id, ativo=True)
        if not perfilacesso.salvar():
            flash("Erro ao salvar o perfil", category="danger")
            break

        # busca a lista de telas liberadas para a empresa
        telascontrato = Telacontrato.query.filter_by(ativo=True,
                                                     contrato_id=empresa.contrato_id).all()
        for telacontrato in telascontrato:
            # cadastro de perfisacesso para o administrador
            telaperfilacesso = TelaPerfilAcesso(perfilacesso_id=perfilacesso.id, tela_id=telacontrato.tela_id)
            if not telaperfilacesso.salvar():
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
        usuario.usuario_administrador(nome=valor['nome'] + "_" + empresa.nome_fantasia + "_" + str(empresa.id),
                                      email=valor['email'], empresa_id=empresa.id,
                                      perfilacesso_id=perfilacesso.id, senha_id=senha.id)

        if usuario.salvar():
            # Se está permitido o envio do email pelo usuario e ignora o email para adminstracao
            if enviar_email and valor['enviar_email']:
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


@empresa_blueprint.route('/gerar_padrao_empresas/', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def gerar_padrao_empresas():
    result, path = arquivo_padrao(nome_arquivo=Empresa.nome_doc, valores=[[x] for x in Empresa.titulos_doc])
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
    else:
        flash("Não foi gerado o arquivo padrão", category="danger")
    return redirect(url_for("empresa.empresa_listar"))


@empresa_blueprint.route('/cadastrar_lote_empresas>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_empresas():
    form = EmpresaForm()

    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Empresa.titulos_doc, encoding='latin-1'))

    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Empresa.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = Empresa.query.filter_by(empresa_gestora_id=current_user.empresa_id).all()
    # tipo de empresa cliente
    tipoempresa = Tipoempresa.query.filter_by(nome='Cliente').one_or_none()

    rejeitados_texto = [['CNPJ', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []
    total = range(df.shape[0])
    # percorre por todas as linhas
    for linha in total:
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados_texto.append(
                    [df.at[linha, 'CNPJ*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])
                rejeitados.append(df.at[linha, 'CNPJ*'])

        # verifica repetições no BD
        for empresa in existentes:
            if empresa.cnpj == df.at[linha, 'CNPJ*'].upper():
                rejeitados.append(df.at[linha, 'CNPJ*'])
                rejeitados_texto.append(
                    [df.at[linha, 'CNPJ*'], "rejeitado devido CNPJ já existir no banco de dados"])
            if empresa.razao_social == df.at[linha, 'Razão_Social*'].upper():
                rejeitados.append(df.at[linha, 'CNPJ*'])
                rejeitados_texto.append(
                    [df.at[linha, 'CNPJ*'], "rejeitado devido RAZÃO SOCIAL já existir no banco de dados"])
            if empresa.nome_fantasia == df.at[linha, 'Nome_Fantasia*'].upper():
                rejeitados.append(df.at[linha, 'CNPJ*'])
                rejeitados_texto.append(
                    [df.at[linha, 'CNPJ*'], "rejeitado devido NOME FANTASIA já existir no banco de dados"])

        # verificar existência do contrato
        contrato = Contrato.query.filter_by(nome=df.at[linha, 'Contrato*'].upper()).one_or_none()
        if not contrato:
            rejeitados.append(df.at[linha, 'CNPJ*'])
            rejeitados_texto.append(
                [df.at[linha, 'CNPJ*'], df.at[linha, 'Contrato*'], "rejeitado devido ao Contrato não existir"])

        # verifica repetições na lista atual
        if df.at[linha, 'CNPJ*'] in aceitos_cod:
            rejeitados.append(df.at[linha, 'CNPJ*'])
            rejeitados_texto.append(
                [df.at[linha, 'CNPJ*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if df.at[linha, 'CNPJ*'] not in rejeitados:
            # altera o valor do subgrupo de nome para id na tabela
            df.at[linha, 'Contrato*'] = contrato.id
            # cria um equipamento e popula ele
            empresa = Empresa()
            for k, v in empresa.titulos_doc.items():
                # recupere o valor
                valor = df.at[linha, k]
                if str(valor).isnumeric() or valor is None:
                    # Salva o atributo se o valor e numerico ou nulo
                    setattr(empresa, v, valor)
                else:
                    # Salva o atributo quando texto
                    setattr(empresa, v, valor.upper())
            # setando as empresas como cliente
            empresa.tipoempresa_id = tipoempresa.id
            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'CNPJ*'])
            # insere o equipamento na lista
            aceitos.append(empresa)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        for empresa in aceitos:
            # salvar a empresa no Banco de dados
            if empresa.salvar():
                # registra os usuários para as empresas
                new_admin(empresa, False)
    flash(f"Total de empresas cadastrados: {len(aceitos)}, rejeitados:{len(total) - len(aceitos)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        result, path = arquivo_padrao(nome_arquivo="Empresas_rejeitadas", valores=rejeitados_texto)
        if result:
            flash(f'Foi gerado o arquivo de empresas rejeitados no caminho: {path}', category="warning")
        else:
            flash("Não foi gerado o arquivo de empresas rejeitados", category="danger")
    return redirect(url_for('empresa.empresa_listar'))


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
                new_admin(empresa, True)
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


@empresa_blueprint.route('/empresa_acessar/<int:empresa_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def empresa_acessar(empresa_id):
    """Função para acesso rápido a empresa subsidiária"""

    empresa = Empresa.query.filter_by(id=empresa_id).one_or_none()

    if empresa:
        if empresa_id != current_user.empresa_id:
            usuario = Usuario.query.filter(
                Usuario.empresa_id == empresa_id,
                Usuario.nome.like("%admin%"),
                Usuario.nome.notlike("%luz%")).one_or_none()
            # caso o usuário exista
            if empresa.ativo:
                if usuario:
                    login_user(usuario)
                    return redirect(url_for('sistema.index'))
                else:
                    flash("Acesso não permitido!", category="danger")
            else:
                flash("Empresa não ativa", category="danger")
        else:
            flash("Empresa atual", category="danger")
    else:
        flash("Empresa não cadastrada", category="danger")

    return redirect(url_for('empresa.empresa_listar'))
