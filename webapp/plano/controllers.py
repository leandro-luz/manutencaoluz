from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import login_required
from .models import db, Plano, Tela, Telaplano
from webapp.plano.forms import PlanoForm, TelaForm, TelaPlanoForm
from webapp.empresa.models import Empresa
from webapp.usuario.models import Perfil, ViewRole
from webapp.usuario import has_view


plano_blueprint = Blueprint(
    'plano',
    __name__,
    template_folder='../templates/sistema/plano',
    url_prefix="/sistema"
)


@plano_blueprint.route('/plan_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_list() -> str:
    """    Função que retorna uma lista de planos    """
    planos = Plano.query.order_by(Plano.nome.asc())  # lista de planos de assinatura em ordem crescente
    return render_template('plan_list.html', planos=planos)


@plano_blueprint.route('/plan_edit/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def plan_edit(plano_id: int):
    """    Função que cadastra ou atualiza um plano de assinatura    """
    if plano_id == 0:
        # --------- CADASTRAR
        plano = Plano()  # instancia um novo plano
        plano.id = 0  # atribui 0 para o id deste novo plano
        form = PlanoForm()  # instância um novo formulário

    else:
        # --------- ATUALIZAR
        plano = Plano.query.filter_by(id=plano_id).first()  # gera uma consulta dos planos cadastrados no banco de dados
        form = PlanoForm(obj=plano)  # inclui a consulta para dentro do formulário

        # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
        form.tela.choices = [(telasplano.id, telasplano.plano.nome) for telasplano
                             in Telaplano.query.filter_by(plano_id=plano_id).all()]  # consulta dos planos com 'id' e nome

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # válida as informações do formulário
        plano.alterar_atributos(form)  # coleta as informações do formulário e insere no plano
        db.session.add(plano)  # adiciona na sessão
        db.session.commit()  # salva no banco de dados

        # --------- MENSAGENS
        if plano_id > 0:
            flash("Plano atualizado", category="success")
        else:
            flash("Plano cadastrado", category="success")
        return redirect(url_for("plano.plan_list"))  # retorna após o cadastro ou atualização
    return render_template("plan_edit.html", form=form, plano=plano)  # retorna caso não esteja validado por algum motivo


@plano_blueprint.route('/viewplan_list/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_list(plano_id: int) -> str:
    """    Função que retorna uma lista de telas de um plano de assinatura    """
    plano = Plano.query.filter_by(id=plano_id).one_or_none()  # instância um plano com base no 'id' de entrada
    telasplano = Telaplano.query.filter_by(plano_id=plano_id).all()  # busca a lista das telas do plano
    return render_template('viewplan_list.html', telasplano=telasplano, plano=plano)


@plano_blueprint.route('/viewplan_edit/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def viewplan_edit(plano_id: int):
    """    Função que edita as telas de um plano de assinatura    """
    form = TelaPlanoForm()  # instância um formulário de telas de planos de assinatura

    # --------- ATUALIZAR AS LISTAS DO FORMULÁRIO
    form.plano.choices = [(planos.id, planos.nome) for planos
                          in Plano.query.filter_by(id=plano_id)]  # lista('id' e nome) de planos com base no 'id'

    form.tela.choices = [(telas.id, telas.nome) for telas in Tela.query.all()]  # lista(id e nome) de todas as telas /
    # cadastradas

    # --------- VALIDAÇÕES E AÇÕES
    if form.validate_on_submit():  # se validado
        telaplano = Telaplano()  # instância uma tela do plano
        telaplano.alterar_atributos(form)  # altera as informaçoes da tela do plano com base no formulário de entrada
        db.session.add(telaplano)  # adiciona a viewplan na sessão
        db.session.commit()  # grava a viewplan no banco de dados

        ids = [[dict(role_name=perfis.nome, role_id=perfis.id, tela_id=telaplano.tela_id)
                for perfis in Perfil.listar_regras_by_empresa(companies.id)]
               for companies in Empresa.listar_empresas_by_plano(telaplano.plano_id)]
        # retorna a lista com todos os perfis que contem o plano alterado
        ViewRole.alterar_perfil(telaplano.active, ids)  # libera a tela e/ou inativa as telas para todo os perfis

        # --------- MENSAGENS
        if plano_id > 0:
            flash("Tela atualizada", category="success")
        return redirect(url_for("plano.viewplan_list", plano_id=plano_id))  # retorna após o cadastro ou atualização
    return render_template("viewplan_edit.html", form=form, id=plano_id)  # retorna caso não seja validado


@plano_blueprint.route('/viewplan_active/<int:telaplano_id>')
@login_required
@has_view('Plano')
def viewplan_active(telaplano_id: int):
    """    Função para ativar/desativar a tela de um plano    """
    telaplano = Telaplano.query.filter_by(id=telaplano_id).one_or_none()  # instância uma tela de um plano a partir do seu

    if telaplano:  # se existir
        telaplano.ativar_desativar()  # ativa e inativa a tela dos planos
        db.session.add(telaplano)  # sala na sessão a tela
        db.session.commit()  # grava no banco de dados

        ids = [[dict(perfil_nome=perfis.nome, perfil_id=perfis.id, tela_id=telaplano.tela_id)
                for perfis in Perfil.listar_regras_by_empresa(companies.id)]
               for companies in Empresa.listar_empresas_by_plano(telaplano.plano_id)]  # retorna a lista com todos os perfis
        # , que contem o plano alterado
        ViewRole.alterar_perfil(telaplano.ativo, ids)  # libera a tela e/ou inativa as telas para todo os perfis

    return redirect(url_for('plano.viewplan_list', plano_id=telaplano.plano_id))


@plano_blueprint.route('/view_list', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_list() -> str:
    """    Função que retorna uma lista de telas em ordem alfabetica    """
    telas = Tela.query.order_by(Tela.plano_id.asc())  # lista de telas
    return render_template('view_list.html', telas=telas)


@plano_blueprint.route('/view_edit/<int:tela_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano')
def view_edit(tela_id: int):
    """    Função que atualiza uma tela de um plano de assinatura    """
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
        tela.alterar_atributos(form)  # altera as informaçoes da tela com base no formulário de entrada
        db.session.add(tela)  # adiciona a tela na sessão
        db.session.commit()  # salva a tela no banco de dados

        # --------- MENSAGENS
        if tela_id > 0:
            flash("Tela atualizada", category="success")
        else:
            flash("Tela cadastrada", category="success")
        return redirect(url_for("plano.view_list"))  # retorna após o cadastro ou atualização
    return render_template("view_edit.html", form=form, tela=tela)  # retorna caso não seja validado por algum motivo
