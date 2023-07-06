from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import login_required
from .models import Contrato, Tela, Telacontrato
from webapp.contrato.forms import ContratoForm, TelaForm, TelaContratoForm
from webapp.empresa.models import Empresa
from webapp.usuario.models import Perfil, Telaperfil
from webapp.usuario import has_view
from webapp.utils.erros import flash_errors
from webapp import db


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
    """    Função que retorna uma lista de planos    """
    contratos = Contrato.query.order_by(Contrato.nome.asc())  # lista de planos de assinatura em ordem crescente
    return render_template('contrato_listar.html', contratos=contratos)


@contrato_blueprint.route('/contrato_editar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def contrato_editar(contrato_id: int):
    """    Função que cadastra ou atualiza um contrato de assinatura    """
    if contrato_id == 0:
        # --------- CADASTRAR
        contrato = Contrato()  # instancia um novo contrato
        contrato.id = 0  # atribui 0 para o id deste novo contrato
        form = ContratoForm()  # instância um novo formulário
        new = True
    else:
        new = False
        # --------- ATUALIZAR
        # gera uma consulta dos planos cadastrados no banco de dados
        contrato = Contrato.query.filter_by(id=contrato_id).first()
        # inclui a consulta para dentro do formulário
        form = ContratoForm(obj=contrato)

        # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
        # consulta das telas para o contrato existente
        form.tela.choices = [(telasplano.id, telasplano.contrato.nome) for telasplano
                             in Telacontrato.query.filter_by(contrato_id=contrato_id).all()]

    # --------- VALIDAÇÕES E AÇÕES
    # válida as informações do formulário
    if form.validate_on_submit():
        # coleta as informações do formulário e insere no contrato
        contrato.alterar_atributos(form)
        if contrato.salvar(new, form):
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
    return render_template("contrato_editar.html", form=form, contrato=contrato)


@contrato_blueprint.route('/contrato_ativar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def contrato_ativar(contrato_id):
    """    Função que ativa/desativa um contrato    """
    # instância um contrato com base no identificador
    contrato = Contrato.query.filter_by(id=contrato_id).one_or_none()
    # se o contrato existir
    if contrato:
        # ativa/inativa o contrato
        contrato.ativar_desativar()
        # salva no banco de dados a alteração
        if contrato.salvar(None, None):
            flash("Contrato ativado/desativado com sucesso", category="success")
        else:
            flash("Contrato não foi ativado/desativado", category="danger")
    else:
        flash("Contrato não registrado", category="danger")
    return redirect(url_for('contrato.contrato_listar'))


@contrato_blueprint.route('/telacontrato_listar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def telacontrato_listar(contrato_id: int) -> str:
    """    Função que retorna uma lista de telas de um contrato de assinatura    """
    # instância um contrato com base no 'id' de entrada
    contrato = Contrato.query.filter_by(id=contrato_id).one_or_none()
    # busca a lista das telas do contrato
    telascontrato = Telacontrato.query.filter_by(contrato_id=contrato_id).all()
    return render_template('telacontrato_listar.html', telascontrato=telascontrato, contrato=contrato)


@contrato_blueprint.route('/telacontrato_editar/<int:contrato_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def telacontrato_editar(contrato_id: int):
    """    Função que edita as telas de um contrato de assinatura    """
    form = TelaContratoForm()  # instância um formulário de telas de planos de assinatura

    # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
    # lista('id' e nome) de planos com base no 'id'
    form.contrato.choices = [(planos.id, planos.nome) for planos
                             in Contrato.query.filter_by(id=contrato_id)]
    #  lista(id e nome) de todas as telas cadastradas
    form.tela.choices = [(telas.id, telas.nome) for telas in Tela.query.all()]

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # se validado
        # instância uma tela do contrato
        telacontrato = Telacontrato()
        # altera as informaçoes da tela do contrato com base no formulário de entrada
        telacontrato.alterar_atributos(form)
        if telacontrato.salvar():

            # retorna a lista com todos os perfis que contem o contrato alterado
            ids = [[dict(perfil_name=perfis.nome, perfil_id=perfis.id, tela_id=telacontrato.tela_id)
                    for perfis in Perfil.listar_regras_by_empresa(companies.id)]
                   for companies in Empresa.listar_empresas_by_plano(telacontrato.contrato_id)]

            # libera a tela e/ou inativa as telas para todo os perfis
            Telaperfil.alterar_perfil(telacontrato.ativo, ids)

            # --------- MENSAGENS
            if contrato_id > 0:
                flash("Tela atualizada", category="success")
            # retorna após o cadastro ou atualização
            return redirect(url_for("contrato.telacontrato_listar", contrato_id=contrato_id))
        else:
            flash("Tela do contrato não foi cadastrada/atualizada", category="danger")
    else:
        flash_errors(form)
    # retorna caso não seja validado
    return render_template("telacontrato_editar.html", form=form, id=contrato_id)


@contrato_blueprint.route('/telacontrato_ativar/<int:telacontrato_id>')
@login_required
@has_view('Contrato')
def telacontrato_ativar(telacontrato_id: int):
    """    Função para ativar/desativar a tela de um contrato    """
    # instância uma tela de um contrato a partir do seu
    telacontrato = Telacontrato.query.filter_by(id=telacontrato_id).one_or_none()

    if telacontrato:  # se existir
        # ativa e inativa a tela dos planos
        telacontrato.ativar_desativar()
        if telacontrato.salvar():

            # retorna a lista com todos os perfis que contem o contrato alterado
            ids = [[dict(perfil_nome=perfis.nome, perfil_id=perfis.id, tela_id=telacontrato.tela_id)
                    for perfis in Perfil.listar_regras_by_empresa(companies.id)]
                   for companies in Empresa.listar_empresas_by_plano(telacontrato.contrato_id)]

            # libera a tela e/ou inativa as telas para todo os perfis
            Telaperfil.alterar_perfil(telacontrato.ativo, ids)
        else:
            flash("Tela do contrato não foi ativada/desativada", category="danger")
    return redirect(url_for('contrato.telacontrato_listar', contrato_id=telacontrato.contrato_id))


@contrato_blueprint.route('/tela_listar', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def tela_listar() -> str:
    """    Função que retorna uma lista de telas em ordem alfabetica    """
    telas = Tela.query.order_by(Tela.plano_id.asc())  # lista de telas
    return render_template('tela_listar.html', telas=telas)


@contrato_blueprint.route('/tela_editar/<int:tela_id>', methods=['GET', 'POST'])
@login_required
@has_view('Contrato')
def tela_editar(tela_id: int):
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
        if tela.salvar():
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
