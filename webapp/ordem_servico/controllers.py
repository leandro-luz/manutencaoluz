from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from webapp.ordem_servico.models import OrdemServico, SituacaoOrdem, FluxoOrdem, TramitacaoOrdem
from webapp.ordem_servico.forms import OrdemServicoForm
from webapp.equipamento.models import Equipamento
from webapp.usuario.models import Usuario
from webapp.usuario import has_view
from webapp.utils.erros import flash_errors

ordem_servico_blueprint = Blueprint(
    'ordem_servico',
    __name__,
    template_folder='../templates/sistema/ordem_servico',
    url_prefix="/sistema"
)


@ordem_servico_blueprint.route('/ordem_listar', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def ordem_listar():
    """Retorna a lista dos planos de manutenção"""
    # ordens = OrdemServico.query.filter(OrdemServico.equipamento.has(Equipamento.empresa_id == current_user.empresa_id))
    ordens = OrdemServico.query.filter(OrdemServico.equipamento_id == Equipamento.id,
                                       Equipamento.empresa_id == current_user.empresa_id).order_by(OrdemServico.codigo.desc())

    return render_template('ordem_servico_listar.html', ordens=ordens)


@ordem_servico_blueprint.route('/ordem_editar/<int:ordem_id>', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def ordem_editar(ordem_id):
    if ordem_id > 0:
        # Atualizar
        ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
        new = False

        if ordem:
            form = OrdemServicoForm(obj=ordem)

            # Atualizar ou Ler dados
            if form.equipamento.data:
                eq_d = form.equipamento.data
                si_d = form.situacaoordem.data

            else:
                eq_d = ordem.equipamento_id
                si_d = ordem.situacaoordem_id


        else:
            flash("Ordem de Serviço não localizado", category="danger")
            return redirect(url_for("ordem_servico.ordem_listar"))

        # Filtro dos status possíveis
        fluxos = FluxoOrdem.query.filter_by(de=si_d).all()
        situacoes = [SituacaoOrdem.query.filter_by(id=fluxo.para).first() for fluxo in fluxos]
        form.situacaoordem.choices = [(0, '')] + [(si.id, si.nome) for si in situacoes]
        form.situacaoordem.data = si_d

        # Lista das tramitações realizadas na ordem de serviço
        tramitacoes = TramitacaoOrdem.query.filter_by(ordemservico_id=ordem.codigo).all()

    else:
        # Cadastrar
        ordem = OrdemServico()
        ordem.id = 0
        form = OrdemServicoForm()
        new = True

        eq_d = form.equipamento.data

        # FILTRA SOMENTE A SITUAÇÃO PENDENTE
        situacao = SituacaoOrdem.query.filter_by(nome="Pendente").one_or_none()
        form.situacaoordem.choices = [(si.id, si.nome) for si in SituacaoOrdem.query.filter_by(nome="Pendente").all()]
        form.situacaoordem.data = situacao.id

    # Listas
    form.equipamento.choices = [(0, '')] + [(eq.id, eq.descricao_curta)
                                            for eq in Equipamento.query.filter_by(empresa_id=current_user.empresa_id)]
    form.equipamento.data = eq_d

    # Validação
    if form.validate_on_submit():
        ordem.alterar_atributos(form, new)
        if ordem.salvar():
            # Mensagens
            if ordem_id > 0:
                flash("Ordem de Serviço Atualizado", category="success")
            else:
                flash("Ordem de Serviço Cadastrado", category="success")
            return redirect(url_for("ordem_servico.ordem_listar"))
        else:
            flash("Ordem de Serviço não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("ordem_servico_editar.html", form=form, ordem=ordem, tramitacoes=tramitacoes)
