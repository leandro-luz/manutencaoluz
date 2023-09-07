import copy
from flask import (render_template, Blueprint, redirect, url_for, flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from webapp.plano_manutencao.models import PlanoManutencao, ListaAtividade, Atividade, TipoBinario, TipoParametro
from webapp.plano_manutencao.forms import AtividadeForm, ListaAtividadeForm
from webapp.ordem_servico.models import OrdemServico, TipoSituacaoOrdem, FluxoOrdem, TramitacaoOrdem, \
    TipoOrdem, TipoSituacaoOrdemPerfilManutentor
from webapp.ordem_servico.forms import OrdemServicoForm, TramitacaoForm
from webapp.equipamento.models import Equipamento, Subgrupo, Grupo
from webapp.usuario.models import PerfilManutentorUsuario, Usuario
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
    """Retorna a lista das ordens de serviços"""

    # Valida se o usuário pode criar ordens de serviços
    lib_solicitante = Usuario.verifica_perfil_manutentor('SOLICITANTE')

    # Lista de ordens quando o usuario é o solicitante
    ordens_by_solicitante = OrdemServico.query.filter(
        OrdemServico.solicitante_id == current_user.id,
        OrdemServico.equipamento_id == Equipamento.id,
        Equipamento.subgrupo_id == Subgrupo.id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id
    )
    # Lista de ordens filtrada pelo tipo de perfil_manutentor do usuario
    ordens_by_perfil = OrdemServico.query.filter(
        OrdemServico.tiposituacaoordem_id == TipoSituacaoOrdemPerfilManutentor.tiposituacaoordem_id,
        TipoSituacaoOrdemPerfilManutentor.perfilmanutentor_id == PerfilManutentorUsuario.perfilmanutentor_id,
        PerfilManutentorUsuario.ativo == True,
        PerfilManutentorUsuario.usuario_id == current_user.id
    )

    # união das listas sem repetições
    ordens_p = list(set(ordens_by_solicitante) | set(ordens_by_perfil))
    # ordenação pelo código
    ordens = sorted(ordens_p, key=lambda ordem: ordem.codigo, reverse=True)

    return render_template('ordem_servico_listar.html', ordens=ordens, lib_solicitante=lib_solicitante)


@ordem_servico_blueprint.route('/ordem_editar/<int:ordem_id>', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def ordem_editar(ordem_id):
    tramitacoes = []
    novas_tramitacoes = []
    atividades = []
    listaatividade_id = 0
    situacao = ''

    # Valida se o usuário pode criar ordens de serviços
    lib_executante = False
    lib_aprovador = False
    lib_fiscalizador = False

    if ordem_id > 0:
        # Valida se o usuário pode criar ordens de serviços
        lib_executante = Usuario.verifica_perfil_manutentor('EXECUTANTE')
        lib_aprovador = Usuario.verifica_perfil_manutentor('APROVADOR')
        lib_fiscalizador = Usuario.verifica_perfil_manutentor('FISCALIZADOR')

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
        fluxos = FluxoOrdem.query.filter_by(de=ordem.tiposituacaoordem_id).all()
        novas_tramitacoes = [TipoSituacaoOrdem.query.filter_by(id=fluxo.para).first() for fluxo in fluxos]

        # Lista das tramitações já realizadas
        tramitacoes = TramitacaoOrdem.query.filter_by(ordemservico_id=ordem.id). \
            order_by(TramitacaoOrdem.data.desc())

        form_atividade = AtividadeForm()
        form_atividade.valorbinario_id.choices = [(0, '')] + [(tb.id, tb.nome) for tb in TipoBinario.query.all()]
        form_atividade.tipoparametro_id.choices = [(0, '')] + [(tp.id, tp.nome) for tp in TipoParametro.query.all()]

        # Atividades a ser executada
        atividades = Atividade.query.filter(
            OrdemServico.id == ordem_id,
            ListaAtividade.id == OrdemServico.listaatividade_id,
            Atividade.listaatividade_id == ListaAtividade.id
        ).all()

        if ordem.listaatividade_id:
            listaatividade_id = ordem.listaatividade_id

    else:
        if not Usuario.verifica_perfil_manutentor('SOLICITANTE'):
            flash("Usuário não permitido criar nova Ordem de Serviço", category="danger")
            return redirect(url_for("ordem_servico.ordem_listar"))
        else:
            # Cadastrar
            ordem = OrdemServico()
            ordem.id = 0
            form = OrdemServicoForm()
            form_tramitacao = TramitacaoForm()
            form_atividade = AtividadeForm()

            new = True

            eq_d = form.equipamento.data

            # FILTRA SOMENTE A SITUAÇÃO PENDENTE
            situacao = TipoSituacaoOrdem.query.filter_by(sigla="AGAP").one_or_none()
            form_tramitacao.tiposituacaoordem.choices = [(si.id, si.nome) for si in
                                                         TipoSituacaoOrdem.query.filter_by(sigla="AGAP").all()]
            form_tramitacao.tiposituacaoordem.data = situacao.id

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

    # Formulario do campo observação
    form_listaatividade = ListaAtividadeForm()

    # Validação
    if form.validate_on_submit():
        ordem.alterar_atributos(form, new)
        # Verificando se o usuário pode executar esta atividade
        if ordem.verificar_ordem_perfil_manutentor():
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
    return render_template("ordem_servico_editar.html", form=form, novas_tramitacoes=novas_tramitacoes, ordem=ordem,
                           tramitacoes=tramitacoes, form_atividade=form_atividade, atividades=atividades,
                           listaatividade_id=listaatividade_id, form_listaatividade=form_listaatividade,
                           lib_executante=lib_executante, lib_aprovador=lib_aprovador,
                           lib_fiscalizador=lib_fiscalizador)


@ordem_servico_blueprint.route('/tramitacao/<int:ordem_id>/<int:tipo_situacao_id>', methods=['GET', 'POST'])
@login_required
@has_view('Ordem de Serviço')
def tramitacao(ordem_id, tipo_situacao_id):
    # Localizar o tipo de tramitação
    tiposituacao = TipoSituacaoOrdem.query.filter_by(id=tipo_situacao_id).one_or_none()
    if tiposituacao:
        # criar uma nova tramitação
        tramitacao = TramitacaoOrdem()
        # registra os valores
        tramitacao.alterar_atributos(ordem_id, tiposituacao.id)
        # salva no banco de dados
        if tramitacao.salvar():

            ordem_antiga = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
            # verifica se a ordem está concluída ou cancelada
            if ordem_antiga.tiposituacaoordem.sigla in ["CONC", "CANC"]:
                # Verifica se a ordem é proviente de um plano de manutenção
                if ordem_antiga.tipoordem.plano:
                    # Verifica se existe um plano
                    plano = PlanoManutencao.query.filter_by(id=ordem_antiga.planomanutencao_id).one_or_none()
                    if plano:
                        # Verifica se está ativo
                        if plano.ativo:
                            # Altera a data prevista
                            plano.alterar_data_prevista(new=False)
                            # Verifica o tipo_data
                            if plano.tipodata.nome == "DATA_MÓVEL":
                                # cria uma nova ordem
                                ordem_nova = OrdemServico()
                                ordem_nova.alterar_atributos_by_ordem(ordem=ordem_antiga, plano=plano)

                                # salva a nova ordem de serviço
                                if ordem_nova.salvar():
                                    plano.salvar()
                                    flash("Ordem de Serviço Cadastrado", category="success")
                                else:
                                    flash("Ordem de Serviço não Cadastrado", category="danger")
                    else:
                        flash("Plano não Cadastrado", category="danger")

                # Gera a nova tramitação automaticamente
                tramitacao = TramitacaoOrdem()
                tiposituacao = TipoSituacaoOrdem.query.filter_by(sigla='AGFI').one_or_none()
                tramitacao.alterar_atributos(ordem_id, tiposituacao.id)
                tramitacao.salvar()

            flash("Tramitação cadastrado", category="success")
        else:
            flash("Erro ao registrar tramitação", category="danger")
    else:
        flash("Tipo de Tramitação não cadastrada", category="danger")

    return redirect(url_for("ordem_servico.ordem_editar", ordem_id=ordem_id))
