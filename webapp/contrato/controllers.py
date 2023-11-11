from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import login_required, current_user

from webapp.contrato.forms import ContratoForm, TelaForm, TelaContratoForm
from webapp.contrato.models import Contrato, Tela, Telacontrato
from webapp.empresa.models import Empresa
from webapp.sistema.models import LogsEventos
from webapp.usuario import has_view
from webapp.usuario.models import TelaPerfilAcesso
from webapp.utils.erros import flash_errors
from webapp.utils.objetos import salvar, excluir

contrato_blueprint = Blueprint(
    'contrato',
    __name__,
    template_folder='../templates/sistema/contrato',
    url_prefix="/sistema"
)


@contrato_blueprint.route('/contrato_listar', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def contrato_listar() -> str:
    LogsEventos.registrar("evento", contrato_listar.__name__)

    """    Função que retorna uma lista de planos    """
    # Montagem do dicionario com os contratos e as quantidade de empresas vinculadas
    lista_contratos = [{'contrato': contrato,
                        'total': Empresa.query.filter(Empresa.contrato_id == contrato.id).count(),
                        'telas': Telacontrato.contagem_telas_ativas(contrato.id)}
                       for contrato in
                       Contrato.query.filter(Contrato.empresa_gestora_id == current_user.empresa_id).order_by(
                           Contrato.nome.asc())]

    form = ContratoForm()

    return render_template('contrato_listar.html', contratos=lista_contratos, form=form)


@contrato_blueprint.route('/contrato_editar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def contrato_editar(contrato_id: int):
    LogsEventos.registrar("evento", contrato_editar.__name__, contrato_id=contrato_id)
    """    Função que cadastra ou atualiza um contrato de assinatura    """
    empresas = []
    telas_liberadas = []
    form_telacontrato = TelaContratoForm()

    if contrato_id > 0:
        # --------- ATUALIZAR
        # gera uma consulta dos planos cadastrados no banco de dados
        contrato = Contrato.query.filter_by(id=contrato_id).first()

        if contrato:
            # inclui a consulta para dentro do formulário
            form = ContratoForm(obj=contrato)
            # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
            # consulta das telas para o contrato existente
            form.tela.choices = [(telasplano.id, telasplano.contrato.nome) for telasplano
                                 in Telacontrato.query.filter_by(contrato_id=contrato_id).all()]

            # Lista de empresas vinculadas ao contrato
            empresas = Empresa.query.filter_by(contrato_id=contrato.id).all()

            # LISTA DAS TELAS PARA O CONTRATO
            # busca a lista das telas do contrato
            telas_liberadas = Telacontrato.query.filter_by(contrato_id=contrato_id).all()

            #  lista(id e nome) de todas as telas cadastradas
            telascontrato = Tela.query.filter(
                Tela.id == Telacontrato.tela_id,
                Telacontrato.contrato_id == current_user.empresa.contrato_id).all()

            # Lista de telas já cadastradas
            telasexistentes = Tela.query.filter(
                Tela.id == Telacontrato.tela_id,
                Telacontrato.contrato_id == contrato_id).all()

            # Lista de telas permitidas sem repetições

            form_telacontrato.tela.choices = [(0, '')] + [(tela.id, tela.nome) for tela in telascontrato if
                                                          tela.id not in {tl.id for tl in telasexistentes}]

        else:
            flash("Contrato não localizado", category="danger")
            return redirect(url_for("contrato.contrato_listar"))

    else:
        # --------- CADASTRAR
        contrato = Contrato()  # instancia um novo contrato
        contrato.id = 0  # atribui 0 para o id deste novo contrato
        form = ContratoForm()  # instância um novo formulário

    # --------- VALIDAÇÕES E AÇÕES
    # válida as informações do formulário
    if form.validate_on_submit():
        # coleta as informações do formulário e insere no contrato
        contrato.alterar_atributos(form)
        if salvar(contrato):
            # --------- MENSAGENS
            if contrato_id > 0:
                flash("Contrato atualizado", category="success")
            else:
                flash("Contrato cadastrado", category="success")
            # retorna após o cadastro ou atualização
            return redirect(url_for("contrato.contrato_listar"))
        else:
            flash("Contrato não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    # retorna caso não esteja validado por algum motivo
    return render_template("contrato_editar.html", form=form, form_telacontrato=form_telacontrato,
                           contrato=contrato, empresas=empresas, telascontrato=telas_liberadas)


@contrato_blueprint.route('/contrato_excluir/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Empresa')
def contrato_excluir(contrato_id):
    LogsEventos.registrar("evento", contrato_excluir.__name__, contrato_id=contrato_id)
    """Função para excluir um contrato"""

    # localizar uma empresa
    contrato = Contrato.localizar_contrato_by_id(contrato_id)
    if contrato:
        if excluir(contrato):
            flash("Contrato excluído", category="success")
        else:
            flash("Erro ao excluir o contrato", category="danger")
    else:
        flash("Contrato não cadastrada", category="danger")
    return redirect(url_for('contrato.contrato_listar'))


@contrato_blueprint.route('/contrato_ativar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def contrato_ativar(contrato_id):
    LogsEventos.registrar("evento", contrato_ativar.__name__, contrato_id=contrato_id)
    """    Função que ativa/desativa um contrato    """
    # instância um contrato com base no identificador
    contrato = Contrato.query.filter_by(id=contrato_id).one_or_none()
    # se o contrato existir
    if contrato:
        ativo = contrato.ativo
        if not ativo:
            # para ativar, verifica se existem telas ativas neste contrato
            if Telacontrato.contagem_telas_ativas(contrato_id) == 0:
                flash("Não permitido ativar sem nenhuma tela ativa para este contrato", category="danger")
                return redirect(url_for('contrato.contrato_listar'))

        # ativa/inativa o contrato
        contrato.ativar_desativar()
        # salva no banco de dados a alteração
        if salvar(contrato):
            if ativo:
                # Busca as empresas vinculadas ao contrato e inativa elas
                Empresa.inativar_by_contrato(contrato_id)
                flash("Contrato desativado com sucesso", category="success")
            else:
                flash("Contrato ativado com sucesso", category="success")
        else:
            flash("Contrato não foi ativado/desativado", category="danger")
    else:
        flash("Contrato não registrado", category="danger")

    return redirect(url_for('contrato.contrato_listar'))


@contrato_blueprint.route('/telacontrato_listar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def telacontrato_listar(contrato_id: int) -> str:
    LogsEventos.registrar("evento", telacontrato_listar.__name__, contrato_id=contrato_id)
    """    Função que retorna uma lista de telas de um contrato de assinatura    """

    # instância um contrato com base no 'id' de entrada
    contrato = Contrato.query.filter_by(id=contrato_id).one_or_none()
    # busca a lista das telas do contrato
    telas_liberadas = Telacontrato.query.filter_by(contrato_id=contrato_id).all()

    #  lista(id e nome) de todas as telas cadastradas
    telascontrato = Tela.query.filter(
        Tela.id == Telacontrato.tela_id,
        Telacontrato.contrato_id == current_user.empresa.contrato_id).all()

    # Lista de telas já cadastradas
    telasexistentes = Tela.query.filter(
        Tela.id == Telacontrato.tela_id,
        Telacontrato.contrato_id == contrato_id).all()

    # Lista de telas permitidas sem repetições
    form = TelaContratoForm()
    form.tela.choices = [(tela.id, tela.nome) for tela in telascontrato if
                         tela.id not in {tl.id for tl in telasexistentes}]

    return render_template('telacontrato_listar.html', telascontrato=telas_liberadas, contrato=contrato, form=form)


@contrato_blueprint.route('/telacontrato_editar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def telacontrato_editar(contrato_id: int):
    LogsEventos.registrar("evento", telacontrato_editar.__name__, contrato_id=contrato_id)
    """    Função que edita as telas de um contrato de assinatura    """

    # instância um formulário de telas de planos de assinatura
    form = TelaContratoForm()
    contrato = Contrato.query.filter_by(id=contrato_id).one_or_none()

    if contrato:
        # instância uma tela do contrato
        telacontrato = Telacontrato()
        if form.validate_on_submit():
            # altera as informaçoes da tela do contrato com base no formulário de entrada
            telacontrato.alterar_atributos(form, contrato_id)
            if salvar(telacontrato):
                flash("Tela do contrato cadastrada", category="success")
            else:
                flash("Erro ao cadastrar tela no contrato", category="danger")
        else:
            flash_errors(form)
    else:
        flash("Contrato não cadastrado", category="danger")

    return redirect(url_for("contrato.contrato_editar", contrato_id=contrato_id))


@contrato_blueprint.route('/telacontrato_excluir/<int:telacontrato_id>/<int:contrato_id>')
@login_required
@has_view('Contrato')
def telacontrato_excluir(telacontrato_id, contrato_id):
    LogsEventos.registrar("evento", telacontrato_excluir.__name__, telacontrato_id=telacontrato_id,
                          contrato_id=contrato_id)
    """    Função para excluir a tela de um contrato    """
    # instância uma tela de um contrato a partir do seu
    telacontrato = Telacontrato.query.filter_by(id=telacontrato_id).one_or_none()

    if telacontrato:  # se existir
        # ativo = telacontrato.ativo
        tela_id = telacontrato.tela_id

        if excluir(telacontrato):
            # quando desativar, verifica os usuario vinculados, se existir
            Telacontrato.verifica_empresas_vinculadas(contrato_id)
            # inativar todas as telas do perfilacesso das empresas vinculadas ao contrato
            TelaPerfilAcesso.inativar_by_contrato(tela_id, contrato_id)
            flash("Tela do contrato foi excluída", category="success")

        else:
            flash("Erro ao excluir a tela do contrato", category="danger")

    return redirect(url_for('contrato.contrato_editar', contrato_id=contrato_id))


@contrato_blueprint.route('/tela_listar', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def tela_listar() -> str:
    LogsEventos.registrar("evento", tela_listar.__name__)
    """    Função que retorna uma lista de telas em ordem alfabetica    """
    telas = Tela.query.order_by(Tela.plano_id.asc())  # lista de telas
    return render_template('tela_listar.html', telas=telas)


@contrato_blueprint.route('/tela_editar/<int:tela_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def tela_editar(tela_id: int):
    LogsEventos.registrar("evento", tela_editar.__name__, tela_id=tela_id)
    """    Função que atualiza uma tela de um contrato de assinatura    """
    if tela_id > 0:
        # --------- ATUALIZAR
        tela = Tela.query.filter_by(id=tela_id).first()  # busca o tela pelo id
        form = TelaForm(obj=tela)  # instância um formulário com base na tela
    else:
        # --------- CADASTRAR
        tela = Tela()  # instância uma tela
        tela.id = 0  # atualiza o valor do id da tela
        form = TelaForm()  # instância o formulário de tela

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # se estiver validado

        # altera as informaçoes da tela com base no formulário de entrada
        tela.alterar_atributos(form)
        if salvar(tela):
            # --------- MENSAGENS
            if tela_id > 0:
                flash("Tela atualizada", category="success")
            else:
                flash("Tela cadastrada", category="success")
            # retorna após o cadastro ou atualização
            return redirect(url_for("contrato.tela_listar"))
        else:
            flash("Tela não cadastrada/atualizada", category="danger")
    else:
        flash_errors(form)
    # retorna caso não seja validado por algum motivo
    return render_template("tela_editar.html", form=form, tela=tela)
