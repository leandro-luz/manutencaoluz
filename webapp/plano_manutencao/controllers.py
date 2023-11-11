import numpy as np
import pandas as pd
from flask import (render_template, Blueprint, redirect, url_for, flash, request, Response)
from flask_login import current_user, login_required

from webapp.empresa.models import Empresa
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo
from webapp.ordem_servico.models import OrdemServico, TipoSituacaoOrdem, TipoOrdem
from webapp.plano_manutencao.forms import PlanoForm, AtividadeForm, ListaAtividadeForm
from webapp.plano_manutencao.models import PlanoManutencao, TipoData, Periodicidade, Atividade, TipoBinario, \
    TipoParametro, ListaAtividade
from webapp.sistema.models import LogsEventos
from webapp.usuario import has_view
from webapp.utils.erros import flash_errors
from webapp.utils.files import lista_para_csv
from webapp.utils.objetos import preencher_objeto_atributos_semvinculo, preencher_objeto_atributos_datas, salvar, \
    excluir

plano_manutencao_blueprint = Blueprint(
    'plano_manutencao',
    __name__,
    template_folder='../templates/sistema/plano_manutencao',
    url_prefix="/sistema"
)


@plano_manutencao_blueprint.route('/listaatividade_preenchida/<int:ordem_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def listaatividade_preenchida(ordem_id):
    LogsEventos.registrar("evento", listaatividade_preenchida.__name__, ordem_id=ordem_id)
    # Localiza a ordem de serviço e verifica se existe
    ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
    if ordem:
        # Localiza e verifica se existem atividades vinculadas nesta ordem de serviço
        atividades = Atividade.query.filter_by(listaatividade_id=ordem.listaatividade_id).all()
        if atividades:
            listaatividade = ListaAtividade.query.filter_by(id=ordem.listaatividade_id).one_or_none()
            return render_template('lista_atividade_preenchida.html', atividades=atividades,
                                   listaatividade=listaatividade, ordem_id=ordem_id)
        else:
            flash("Atividades não cadastradas nesta ordem de serviço!", category="danger")
            return redirect(url_for("ordem_servico.ordem_editar", ordem_id=ordem_id))
    else:
        flash("Ordem de Serviço não cadastrada!", category="danger")
        return redirect(url_for("ordem_servico.ordem_editar", ordem_id=ordem_id))


@plano_manutencao_blueprint.route(
    '/atividade_editar/<int:plano_id>/<int:listaatividade_id>/<int:atividade_id>/<tipo>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def atividade_editar(plano_id, listaatividade_id, atividade_id, tipo):
    LogsEventos.registrar("evento", atividade_editar.__name__, plano_id=plano_id, listaatividade_id=listaatividade_id,
                          atividade_id=atividade_id, tipo=tipo)
    lista_new = False
    listaatividade = ListaAtividade()
    atividade = Atividade()
    form_atividade = AtividadeForm()
    total = 0
    atualizar_revisao = False

    if atividade_id > 0:
        # Verifica se a atividade existe no BD
        atividade = Atividade.query.filter_by(id=atividade_id).one_or_none()
        if atividade:
            if tipo == "excluir":
                if excluir(atividade):
                    lista_new = True
                else:
                    flash("Erro ao excluir a atividades", category="danger")
            else:
                if tipo == "descer":
                    atividade.posicao += 1
                if tipo == "subir":
                    if atividade.posicao > 1:
                        atividade.posicao -= 1
                if atividade.salvar():
                    flash("Atividade alterada com sucesso!", category="warning")
                else:
                    flash("Erro ao alterar a atividades", category="danger")

                return redirect(url_for("plano_manutencao.plano_editar", plano_id=plano_id))

    if listaatividade_id > 0:
        # busca a lista de atividades
        listaatividade = ListaAtividade.query.filter_by(id=listaatividade_id).one_or_none()
        # Verifica se a lista de atividades existe
        if listaatividade:

            # calcula o total de ordens vinculadas a esta lista
            total = ListaAtividade.query.filter(
                ListaAtividade.nome == listaatividade.nome,
                OrdemServico.listaatividade_id == ListaAtividade.id
            ).count()

            # se não houver ordens de serviços vinculadas a lista
            if total == 0:
                # vincula a lista de atividade na atividade,
                form_atividade.listaatividade_id.data = listaatividade_id
            else:
                lista_new = True
        else:
            flash("Lista de Atividades não encontrada", category="danger")
            return redirect(url_for("plano_manutencao.plano_editar", plano_id=plano_id))

    # Cria uma nova listaatividade
    if listaatividade_id == 0 or lista_new:
        listaatividade_id_nova = 0
        if total > 0:
            # Gera as copias das atividades caso exista OS vinculadas nesta nova lista
            listaatividade_id_nova = ListaAtividade.copiar_lista(listaatividade_id, True)
            listaatividade = ListaAtividade.query.filter_by(id=listaatividade_id_nova).one_or_none()

        # se não houver
        if listaatividade_id_nova == 0 and listaatividade_id == 0:
            listaatividade = ListaAtividade()
            listaatividade.alterar_atributos()
            if listaatividade.salvar():
                form_atividade.listaatividade_id.data = listaatividade.id
            else:
                flash("Erro ao cadastrar nova lista de atividades", category="danger")
                return redirect(url_for("plano_manutencao.plano_editar", plano_id=plano_id))
        else:
            listaatividade = ListaAtividade.query.filter_by(id=listaatividade.id).one_or_none()
            form_atividade.listaatividade_id.data = listaatividade.id
            atualizar_revisao = True

        if tipo == "excluir":
            # Verifica se o plano existe
            plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
            if plano:
                # Alterar a referencia da lista no plano
                if listaatividade_id_nova > 0:
                    plano.alterar_lista(listaatividade.id, True)

                # Calcula a quantidade de atividades na lista
                total_atv = Atividade.query.filter_by(listaatividade_id=listaatividade.id).count()
                # se não houver atividades o plano ficará inativo
                if total_atv == 0:
                    plano.ativar_desativar()
                    plano.salvar()
                    flash("Plano de Manutenção Inativado por falta de atividades!", category="warning")

            flash("Atividade excluída com sucesso!", category="warning")
            return redirect(url_for("plano_manutencao.plano_editar", plano_id=plano_id))

    # validar as informações da atividade
    if form_atividade.validate_on_submit():
        atividade.alterar_atributos(form_atividade)
        # salvar a atividade
        if atividade.salvar():
            # vincular a lista da atividade no plano de manutenção
            plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
            if plano:
                # alterar a listaatividade do plano
                plano.alterar_lista(listaatividade.id, atualizar_revisao)
            flash("Atividade cadastrada no plano de manutenção", category="success")
        else:
            # Se ocorrer um erro ao salvar a atividade, exclui
            # if lista_new:
            #     listaatividade.excluir()
            flash("Atividade não cadastrada", category="danger")
    else:
        flash_errors(form_atividade)
    return redirect(url_for("plano_manutencao.plano_editar", plano_id=plano_id))


@plano_manutencao_blueprint.route('/listaatividade_editar/<int:ordem_id>/<int:listaatividade_id>/<tramitacao_sigla>/',
                                  methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def listaatividade_editar(ordem_id, listaatividade_id, tramitacao_sigla):
    LogsEventos.registrar("evento", listaatividade_editar.__name__, ordem_id=ordem_id,
                          listaatividade_id=listaatividade_id,
                          tramitacao_sigla=tramitacao_sigla)
    form_listaatividade = ListaAtividadeForm()

    # verifica a existência da ordem de serviço
    ordem = OrdemServico.query.filter_by(id=ordem_id).one_or_none()
    if ordem:

        # verifica se a ordem não é proveniente de um plano
        observacao = form_listaatividade.observacao.data
        if not ordem.tipoordem.plano:
            #   cria uma listaatividade nova
            listaatividade = ListaAtividade()
            listaatividade.alterar_atributos()

            if listaatividade:
                tipo_situacao = TipoSituacaoOrdem.query.filter_by(sigla=tramitacao_sigla).one_or_none()
                if tipo_situacao:
                    # vincula a listaatividade na ordem
                    ordem.listaatividade_id = listaatividade.id
                    if not ordem.salvar():
                        flash("Erro ao atualizar a ordem de serviço", category="danger")

                    # Salvar as informações do campo observação
                    listaatividade.alterar_observacao(observacao)
                    if not listaatividade.salvar():
                        flash("Erro ao salvar nova lista de atividades", category="danger")

                    # gera a nova tramitação
                    return redirect(
                        url_for("ordem_servico.tramitacao", ordem_id=ordem_id, tipo_situacao_id=tipo_situacao.id))
                else:
                    flash("Tipo Situação não cadastrada", category="danger")
            else:
                flash("Lista de atividades não cadastrada", category="danger")

        else:
            # verifica a existencia da lista de atividade
            listaatividade = ListaAtividade.query.filter_by(id=listaatividade_id).one_or_none()
            if listaatividade:
                # verifica a existencia do tipo de situação da ordem
                tipo_situacao = TipoSituacaoOrdem.query.filter_by(sigla=tramitacao_sigla).one_or_none()
                if tipo_situacao:
                    # instanciar o formulário
                    form_atividade = AtividadeForm()

                    # coletar as atividades da lista
                    atividades = Atividade.query.filter(
                        OrdemServico.id == ordem_id,
                        ListaAtividade.id == OrdemServico.listaatividade_id,
                        Atividade.listaatividade_id == ListaAtividade.id
                    ).all()

                    # coletar os valores preenchidos
                    string_valores = request.form['valores']
                    list_valores = string_valores.split(";")

                    for x in range(len(atividades)):
                        # coletar o tipo de valor
                        tipo_valor = list_valores[x].split(":")
                        # inserir o valor no local correto do objeto
                        match tipo_valor[0]:
                            case 'valorbinario_id':
                                atividades[x].valorbinario_id = tipo_valor[1]
                            case 'valorinteiro':
                                atividades[x].valorinteiro = tipo_valor[1]
                            case 'valordecimal':
                                atividades[x].valordecimal = tipo_valor[1]
                            case 'valortexto':
                                atividades[x].valortexto = tipo_valor[1]
                        # salvar a atividade
                        if not atividades[x].salvar():
                            flash("Valores da atividade não registrado", category="danger")

                    # Salvar as informações do campo observação
                    listaatividade.alterar_observacao(form_listaatividade.observacao.data)

                    # gera a nova tramitação
                    return redirect(
                        url_for("ordem_servico.tramitacao", ordem_id=ordem_id, tipo_situacao_id=tipo_situacao.id))
                else:
                    flash("Tipo de Tramitação não cadastrada", category="danger")
            else:
                flash("Lista de Atividades não cadastrada", category="danger")
    else:
        flash("Ordem de Serviço não cadastrada", category="danger")

    return redirect(url_for("ordem_servico.ordem_listar"))


@plano_manutencao_blueprint.route('/plano_listar', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_listar():
    LogsEventos.registrar("evento", plano_listar.__name__)
    """Retorna a lista dos planos de manutenção"""
    planos = PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id).all()
    return render_template('plano_manutencao_listar.html', planos=planos)


@plano_manutencao_blueprint.route('/plano_ativar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_ativar(plano_id):
    LogsEventos.registrar("evento", plano_ativar.__name__, plano_id=plano_id)
    plano = PlanoManutencao.query.filter_by(id=plano_id).one_or_none()
    # Verifica se o plano está cadastrado
    if plano:
        # Verifica se o plano está ativado
        if plano.ativo:
            # Desativar o plano
            plano.ativar_desativar()
            if plano.salvar():
                flash("Plano de Manutenção Desativado", category="success")
            else:
                flash("Plano de Manutenção não ativado/desativado", category="danger")
        else:
            # Verifica se o plano tem lista de atividade cadastrada
            if plano.listaatividade_id:
                # Verifica se a listaatividades tem atividades cadastradas
                if Atividade.query.filter_by(listaatividade_id=plano.listaatividade_id).count() > 0:
                    # Verifica se existe ordem de serviço do tipo "DATA_MOVEL" já criada para este plano
                    ordens = OrdemServico.query.filter(
                        OrdemServico.planomanutencao_id == plano.id,
                        PlanoManutencao.id == OrdemServico.planomanutencao_id,
                        TipoData.id == PlanoManutencao.tipodata_id,
                        TipoData.nome == "DATA_MÓVEL"
                    ).all()

                    # Caso não haja criar a primeira ordem do plano
                    if not ordens:
                        ordem = OrdemServico()
                        ordem.alterar_atributos_by_plano(plano)
                        # salva a nova ordem de serviço
                        if ordem.salvar():
                            flash("Ordem de Serviço Cadastrado", category="success")
                            # criar a primeira tramitação
                            tipo_situacao = TipoSituacaoOrdem.query.filter_by(sigla="AGEX").one_or_none()
                            return redirect(
                                url_for("ordem_servico.tramitacao", ordem_id=ordem.id,
                                        tipo_situacao_id=tipo_situacao.id))
                        else:
                            flash("Ordem de Serviço não Cadastrado", category="danger")
                    # Ativa o plano
                    plano.ativar_desativar()
                    if plano.salvar():
                        flash("Plano de Manutenção Ativado", category="success")
                    else:
                        flash("Plano de Manutenção não ativado/desativado", category="danger")
                else:
                    flash("Lista de Atividades sem nenhuma atividade cadastrada", category="danger")
            else:
                flash("Lista de Atividades ainda não cadastrada para este plano", category="danger")
    else:
        flash("Plano de Manutenção não localizado", category="danger")
    return redirect(url_for('plano_manutencao.plano_listar'))


@plano_manutencao_blueprint.route('/plano_editar/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def plano_editar(plano_id):
    LogsEventos.registrar("evento", plano_editar.__name__, plano_id=plano_id)
    new = True
    atividades = []
    listaatividade_id = 0

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
            # verifica se o plano tem lista de atividades
            if plano.listaatividade_id:
                listaatividade_id = plano.listaatividade_id

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
            # Lista de atividades vinculado ao plano de manutenção
            atividades = Atividade.query.filter_by(listaatividade_id=listaatividade_id) \
                .order_by(Atividade.posicao.asc()).all()

            form_atividade = AtividadeForm()
            form_atividade.posicao.data = len(atividades) + 1
            form_atividade.valorbinario_id.choices = [(0, '')] + [(tb.id, tb.nome) for tb in TipoBinario.query.all()]
            form_atividade.tipoparametro_id.choices = [(0, '')] + [(tp.id, tp.nome) for tp in TipoParametro.query.all()]

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

        form_atividade = AtividadeForm()

    # Listas
    form.tipoordem.choices = [(0, '')] + [(to.id, to.nome) for to in TipoOrdem.query.filter_by(plano=True)]
    form.tipodata.choices = [(tp.id, tp.nome) for tp in TipoData.query.all()]
    form.periodicidade.choices = [(0, '')] + [(p.id, p.nome) for p in Periodicidade.query.all()]

    form.equipamento.choices = [(0, '')] + [(e.id, e.descricao_curta)
                                            for e in Equipamento.query.filter(Equipamento.subgrupo_id == Subgrupo.id,
                                                                              Subgrupo.grupo_id == Grupo.id,
                                                                              Grupo.empresa_id == Empresa.id,
                                                                              Empresa.id == current_user.empresa_id)
                                            ]
    form.tipoordem.data = to_d
    form.tipodata.data = tp_d
    form.equipamento.data = e_d
    form.periodicidade.data = p_d

    # Validação
    if form.validate_on_submit():
        plano.alterar_atributos(form, new)
        if plano.salvar():
            # Mensagens
            if plano_id > 0:
                flash("Plano de manutenção atualizado", category="success")
            else:
                flash("Plano de manutenção cadastrado, mas deve incluir uma lista de atividades para ser ativado",
                      category="success")
            return redirect(url_for("plano_manutencao.plano_listar"))
        else:
            flash("Plano de manutenção não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)

    return render_template("plano_manutencao_editar.html", form=form, plano=plano, plano_id=plano.id,
                           listaatividade_id=listaatividade_id, atividades=atividades,
                           form_atividade=form_atividade)


@plano_manutencao_blueprint.route('/gerar_padrao_planos_manutencao/', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def gerar_padrao_planos_manutencao():
    LogsEventos.registrar("evento", gerar_padrao_planos_manutencao.__name__)

    """Função que gera o arquivo padrão para o cadastro em lote"""
    csv_data = lista_para_csv([[x] for x in PlanoManutencao.titulos_doc], None)
    nome = "tabela_base_plano_manutencao.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"})


@plano_manutencao_blueprint.route('/gerar_csv_planos/', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def gerar_csv_planos():
    LogsEventos.registrar("evento", gerar_csv_planos.__name__)
    # Gera o arquivo csv com os titulos

    csv_data = lista_para_csv([[x] for x in PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id).all()], PlanoManutencao.titulos_csv)

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=planos_manutencao.csv'}
    )


@plano_manutencao_blueprint.route('/plano_excluir/<int:plano_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def plano_excluir(plano_id):
    LogsEventos.registrar("evento", plano_excluir.__name__, plano_id=plano_id)

    plano = PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id,
        PlanoManutencao.id == plano_id
    ).one_or_none()

    if plano:
        if excluir(plano):
            flash("Plano de Manutenção excluído", category="success")
        else:
            flash("Erro ao excluir o Plano de Manutenção", category="danger")
    else:
        flash("Plano não cadastrado não cadastrado", category="danger")

    return redirect(url_for('plano_manutencao.plano_listar'))


@plano_manutencao_blueprint.route('/cadastrar_lote_planos_manutencao/', methods=['GET', 'POST'])
@login_required
@has_view('Plano de Manutenção')
def cadastrar_lote_planos_manutencao():
    LogsEventos.registrar("evento", cadastrar_lote_planos_manutencao.__name__)

    form = PlanoForm()

    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=PlanoManutencao.titulos_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in PlanoManutencao.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.nome for x in PlanoManutencao.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id,
        Equipamento.id == PlanoManutencao.equipamento_id).all()]

    rejeitados_texto = [['NOME', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []
    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # Verifica se o titulo não está no arquivo em lote
        if df.at[linha, 'Nome*'] == 'NOME*':
            continue
        else:
            # verifica se os campo obrigatórios foram preenchidos
            for col_ob in titulos_obrigatorio:
                # caso não seja
                if not df.at[linha, col_ob]:
                    # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Nome*'] in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado por já existir no banco de dados"])

        # Verifica se o equipamento existe para a empresa
        equipamento = Equipamento.localizar_equipamento_by_nome(current_user.empresa_id,
                                                                df.at[linha, 'Equipamento_descricao_curta*'])
        if not equipamento:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao equipamento não existir"])

        periodicidade = Periodicidade.query.filter(
            Periodicidade.nome == df.at[linha, 'Periodicidade*']).one_or_none()
        if not periodicidade:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido a periodicidade não existir"])

        tipo_data = TipoData.query.filter(
            TipoData.nome == df.at[linha, 'Tipo_Data_Inicial*']).one_or_none()
        if not tipo_data:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao tipo_data_inicial não existir"])

        tipo_ordem = TipoOrdem.query.filter(
            TipoOrdem.nome == df.at[linha, 'Tipo_Ordem*']).one_or_none()
        if not tipo_ordem:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao tipo_ordem não existir"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Nome*'] in aceitos_cod:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # cria um plano_manutenção e popula ele
            plano = PlanoManutencao()
            # preeche os atributos diretamente
            plano = preencher_objeto_atributos_semvinculo(plano, plano.titulos_valor, df, linha)
            # preeche os atributos de datas
            plano = preencher_objeto_atributos_datas(plano, plano.titulos_data, df, linha)
            # altera o valor do equipamento,periodicidade,tipo_data,tipo_ordem de nome para id na tabela
            plano.equipamento_id = equipamento.id
            plano.periodicidade_id = periodicidade.id
            plano.tipodata_id = tipo_data.id
            plano.tipoordem_id = tipo_ordem.id

            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Nome*'])
            # insere o equipamento na lista
            aceitos.append(plano)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        salvar(aceitos)

    flash(f"Total de plano cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto) - 1}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 1:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)

        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=planosmanutencao_rejeitados.csv'})

    return redirect(url_for('plano_manutencao.plano_listar'))
