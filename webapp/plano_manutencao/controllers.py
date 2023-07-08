from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from webapp.plano_manutencao.models import PlanoManutencao, TipoData, Periodicidade
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo
from webapp.ordem_servico.models import OrdemServico, SituacaoOrdem, FluxoOrdem, TramitacaoOrdem, TipoOrdem
from webapp.ordem_servico.forms import OrdemServicoForm
from webapp.plano_manutencao.forms import PlanoForm
from webapp.usuario import has_view
from webapp.ordem_servico.models import TipoOrdem
from webapp.utils.erros import flash_errors

plano_manutencao_blueprint = Blueprint(
    'plano_manutencao',
    __name__,
    template_folder='../templates/sistema/plano_manutencao',
    url_prefix="/sistema"
)


@plano_manutencao_blueprint.route('/plano_listar', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_listar():
    """Retorna a lista dos planos de manutenção"""
    planos = PlanoManutencao.query.filter_by(empresa_id=current_user.empresa_id).all()
    return render_template('plano_manutencao_listar.html', planos=planos)


@plano_manutencao_blueprint.route('/plano_ativar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_ativar(plano_id):
    plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
    if plano:
        plano.ativar_desativar()
        if not plano.salvar():
            flash("Plano de Manutenção não ativado/desativado", category="danger")
    else:
        flash("Plano de Manutenção não localizado", category="danger")
    return redirect(url_for('plano_manutencao.plano_listar'))


@plano_manutencao_blueprint.route('/plano_editar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_editar(plano_id):
    new = True
    if plano_id > 0:
        # Atualizar
        plano = PlanoManutencao.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == Equipamento.subgrupo_id,
            Equipamento.id == PlanoManutencao.equipamento_id,
            PlanoManutencao.id == plano_id
        ).one_or_none()

        # verifica se o plano existe
        if plano:
            form = PlanoForm(obj=plano)
            new = False
            # Atualizar ou Ler dados
            if form.tipodata.data:
                to_d = form.tipoordem.data
                tp_d = form.tipodata.data
                e_d = form.equipamento.data
                p_d = form.periodicidade.data
            else:
                to_d = plano.tipoordem_id
                tp_d = plano.tipodata_id
                e_d = plano.equipamento_id
                p_d = plano.periodicidade_id
        else:
            flash("Plano de manutenção não localizado", category="danger")
            return redirect(url_for("plano_manutencao.plano_listar"))
    else:
        # Cadastrar
        plano = PlanoManutencao()
        plano.id = 0
        form = PlanoForm()

        tp_d = form.tipodata.data
        e_d = form.equipamento.data
        p_d = form.periodicidade.data
        to_d = form.tipoordem.data

    # Listas
    form.tipoordem.choices = [(0, '')] + [(to.id, to.nome) for to in TipoOrdem.query.filter_by(plano=True)]
    form.tipodata.choices = [(tp.id, tp.nome) for tp in TipoData.query.all()]
    form.periodicidade.choices = [(0, '')] + [(p.id, p.nome) for p in Periodicidade.query.all()]
    form.equipamento.choices = [(0, '')] + [(e.id, e.descricao_curta) for e in Equipamento.query.all()]

    form.tipoordem.data = to_d
    form.tipodata.data = tp_d
    form.equipamento.data = e_d
    form.periodicidade.data = p_d

    # Validação
    if form.validate_on_submit():
        plano.alterar_atributos(form)
        if plano.salvar():

            # case seja um novo plano, gera um ordem para este plano
            if new:
                # recupera o plano salvo
                plano = PlanoManutencao.query.filter_by(nome=form.nome.data).one_or_none()
                ordem = OrdemServico()

                # insere as informações da ordem de serviço do novo plano
                form_os = OrdemServicoForm()
                form_os.descricao.data = plano.nome
                form_os.tipo.data = plano.tipoordem_id
                form_os.equipamento.data = plano.equipamento_id
                ordem.planomanutencao_id = plano.id
                ordem.alterar_atributos(form_os, new, plano.data_inicio)

                # salva a nova ordem de serviço
                if ordem.salvar():
                    flash("Ordem de Serviço Cadastrado", category="success")
                else:
                    flash("Ordem de Serviço não Cadastrado", category="success")

            # Mensagens
            if plano_id > 0:
                flash("Plano de manutenção atualizado", category="success")
            else:
                flash("Plano de manutenção cadastrado", category="success")
            return redirect(url_for("plano_manutencao.plano_listar"))
        else:
            flash("Plano de manutenção não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("plano_manutencao_editar.html", form=form, plano=plano)
