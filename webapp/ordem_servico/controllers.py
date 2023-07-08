from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from webapp.plano_manutencao.models import PlanoManutencao
from webapp.ordem_servico.models import OrdemServico, SituacaoOrdem, FluxoOrdem, TramitacaoOrdem, TipoOrdem
from webapp.ordem_servico.forms import OrdemServicoForm, TramitacaoForm
from webapp.equipamento.models import Equipamento, Subgrupo, Grupo
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
    ordens = OrdemServico.query.filter(
        OrdemServico.equipamento_id == Equipamento.id,
        Equipamento.subgrupo_id == Subgrupo.id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Equipamento.descricao_curta).order_by(
        OrdemServico.codigo.desc())
    return render_template('ordem_servico_listar.html', ordens=ordens)


@ordem_servico_blueprint.route('/ordem_editar/<int:ordem_id>', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def ordem_editar(ordem_id):
    tramitacoes = []
    situacao = ''
    if ordem_id > 0:
        # Atualizar
        new = False

        ordem = OrdemServico.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == Equipamento.subgrupo_id,
            Equipamento.id == OrdemServico.equipamento_id,
            OrdemServico.id == ordem_id
        ).one_or_none()

        # verifica se a ordem existe
        if ordem:
            form = OrdemServicoForm(obj=ordem)
            form_tramitacao = TramitacaoForm()

            # Atualizar ou Ler dados
            if form.equipamento.data:
                eq_d = form.equipamento.data
            else:
                eq_d = ordem.equipamento_id

        else:
            flash("Ordem de Serviço não localizado", category="danger")
            return redirect(url_for("ordem_servico.ordem_listar"))

        # Filtro dos status possíveis
        fluxos = FluxoOrdem.query.filter_by(de=ordem.situacaoordem_id).all()
        situacoes = [SituacaoOrdem.query.filter_by(id=fluxo.para).first() for fluxo in fluxos]
        form_tramitacao.situacaoordem.choices = [(0, '')] + [(si.id, si.nome) for si in situacoes]
        form_tramitacao.situacaoordem.data = ordem.situacaoordem_id

        # Lista das tramitações realizadas na ordem de serviço
        tramitacoes = TramitacaoOrdem.query.filter_by(ordemservico_id=ordem.id). \
            order_by(TramitacaoOrdem.data.desc())
    else:
        # Cadastrar
        ordem = OrdemServico()
        ordem.id = 0
        form = OrdemServicoForm()
        form_tramitacao = TramitacaoForm()
        new = True

        eq_d = form.equipamento.data

        # FILTRA SOMENTE A SITUAÇÃO PENDENTE
        situacao = SituacaoOrdem.query.filter_by(nome="Pendente").one_or_none()
        form_tramitacao.situacaoordem.choices = [(si.id, si.nome) for si in
                                                 SituacaoOrdem.query.filter_by(nome="Pendente").all()]
        form_tramitacao.situacaoordem.data = situacao.id

        form.tipo.choices = [(0, '')] + [(tipo.id, tipo.nome)
                                         for tipo in TipoOrdem.query.filter_by(plano=False)]

    # Listas
    equipamentos = Equipamento.query.filter(
        Equipamento.subgrupo_id == Subgrupo.id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Equipamento.descricao_curta).order_by(
        Equipamento.descricao_curta.desc())
    form.equipamento.choices = [(0, '')] + [(eq.id, eq.descricao_curta) for eq in equipamentos]
    form.equipamento.data = eq_d

    # Validação
    if form.validate_on_submit():
        ordem.alterar_atributos(form, new)
        if ordem.salvar():
            # Mensagens
            if ordem_id > 0:
                flash("Ordem de Serviço Atualizado", category="success")
            else:
                TramitacaoOrdem.insere_tramitacao(form.descricao.data, situacao, "ABERTURA DA ORDEM DE SERVIÇO")

                flash("Ordem de Serviço Cadastrado", category="success")
            return redirect(url_for("ordem_servico.ordem_listar"))
        else:
            flash("Ordem de Serviço não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("ordem_servico_editar.html", form=form, form_tramitacao=form_tramitacao, ordem=ordem,
                           tramitacoes=tramitacoes)


@ordem_servico_blueprint.route('/tramitacao/<int:ordem_id>', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def tramitacao(ordem_id):
    form_tramitacao = TramitacaoForm()
    tramitacao_ = TramitacaoOrdem()

    if form_tramitacao.validate_on_submit():
        tramitacao_.alterar_atributos(form_tramitacao, ordem_id)
        if tramitacao_.salvar():
            flash("Tramitação cadastrado", category="success")

            ordem_antiga = OrdemServico.query.filter_by(id=ordem_id).one_or_none()

            # verifica se a Ordem está concluída
            situacao = ordem_antiga.situacaoordem.nome
            if situacao == "Concluída" or situacao == "Cancelada":
                # Verifica se o plano está ativo
                plano = PlanoManutencao.query.filter_by(id=ordem_antiga.planomanutencao_id).one_or_none()
                if plano.ativo:

                    # Verifica o tipo_data
                    if plano.tipodata.nome == "Data_Móvel":
                        tempo = plano.periodicidade.tempo
                        unidade = plano.periodicidade.unidade.nome
                        # Calcula a data prevista
                        dta_prevista = ordem_antiga.data_futura(tempo, unidade)

                        # insere as informações da ordem de serviço do novo plano
                        form_os = OrdemServicoForm()
                        ordem_nova = OrdemServico()

                        form_os.descricao.data = ordem_antiga.descricao
                        form_os.tipo.data = ordem_antiga.tipoordem_id
                        form_os.equipamento.data = ordem_antiga.equipamento_id
                        ordem_nova.planomanutencao_id = ordem_antiga.id
                        ordem_nova.alterar_atributos(form_os, True, dta_prevista)

                        # salva a nova ordem de serviço
                        if ordem_nova.salvar():
                            flash("Ordem de Serviço Cadastrado", category="success")
                        else:
                            flash("Ordem de Serviço não Cadastrado", category="success")

        else:
            flash("Tramitação não cadastrado", category="danger")
    else:
        flash_errors(form_tramitacao)

    return redirect(url_for("ordem_servico.ordem_editar", ordem_id=ordem_id))
