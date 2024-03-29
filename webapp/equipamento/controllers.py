import io
import zipfile

import numpy as np
import pandas as pd
from flask import render_template, Blueprint, redirect, url_for, flash, Response, jsonify, request
from flask_login import current_user, login_required

from webapp.empresa.models import Empresa
from webapp.equipamento.forms import EquipamentoForm, GrupoForm, SubgrupoForm, LocalizacaoForm, AgrupamentoForm
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo, Pavimento, Setor, Local, Area, Volume, Vazao, \
    Comprimento, Peso, Potencia, TensaoEletrica, preencher_objeto_atributos_comvinculo
from webapp.sistema.models import LogsEventos
from webapp.usuario import has_view
from webapp.utils.erros import flash_errors
from webapp.utils.files import lista_para_csv
from webapp.utils.objetos import salvar, excluir, preencher_objeto_atributos_semvinculo, \
    preencher_objeto_atributos_booleanos, preencher_objeto_atributos_datas, criptografar_id_lista
from webapp.utils.tools import descriptografar, criptografar

equipamento_blueprint = Blueprint(
    'equipamento',
    __name__,
    template_folder='../templates/sistema/equipamento',
    url_prefix="/sistema"
)


# EQUIPAMENTO ----------------------------------------------------------------------------------------

@equipamento_blueprint.route('/equipamento_listar', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_listar():
    LogsEventos.registrar("evento", equipamento_listar.__name__)
    """Retorna a lista de equipamentos"""
    equipamentos = Equipamento.query.filter(
        Equipamento.subgrupo_id == Subgrupo.id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Equipamento.cod)

    criptografar_id_lista(equipamentos)

    return render_template('equipamento_listar.html', equipamentos=equipamentos)


@equipamento_blueprint.route('/equipamento_editar/<equipamento_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_editar(equipamento_id_crypto):
    # Decriptografar os ids
    equipamento_id = descriptografar(equipamento_id_crypto)

    LogsEventos.registrar("evento", equipamento_editar.__name__, equipamento_id=equipamento_id)
    """Função para editar um equipamento"""
    grupo_id = 0
    subgrupo_id = 0
    new = True
    equipamento = Equipamento()

    if equipamento_id > 0:
        new = False
        equipamento = Equipamento.localizar_equipamento_by_id(current_user.empresa_id, equipamento_id)

        # verifica se o equipamento existe e se pertence a empresa do usuário
        if equipamento:
            equipamento.id_criptografado = equipamento_id_crypto
            form = EquipamentoForm(obj=equipamento)
            grupo_id = criptografar(str(equipamento.subgrupo.grupo_id))
            subgrupo_id = criptografar(str(equipamento.subgrupo_id))
            # Atualizar ou Ler dados
            if form.grupo.data:
                g_d = form.grupo.data
                sg_d = form.subgrupo.data
                st_d = form.setor.data
                lo_d = form.local.data
                pv_d = form.pavimento.data
                ar_d = form.und_area.data
                vo_d = form.und_volume.data
                va_d = form.und_vazao.data
                la_d = form.und_largura.data
                al_d = form.und_altura.data
                co_d = form.und_comprimento.data
                pe_d = form.und_peso.data
                po_d = form.und_potencia.data
                te_d = form.und_tensao.data

            else:
                g_d = equipamento.subgrupo.grupo_id
                sg_d = equipamento.subgrupo_id
                st_d = equipamento.setor_id
                lo_d = equipamento.local_id
                pv_d = equipamento.pavimento_id
                ar_d = equipamento.und_area_id
                vo_d = equipamento.und_volume_id
                va_d = equipamento.und_vazao_id
                la_d = equipamento.und_largura_id
                al_d = equipamento.und_altura_id
                co_d = equipamento.und_comprimento_id
                pe_d = equipamento.und_peso_id
                po_d = equipamento.und_potencia_id
                te_d = equipamento.und_tensao_id

        else:
            flash("Equipamento não localizado", category="danger")
            return redirect(url_for("equipamento.equipamento_listar"))
    else:
        # Cadastrar
        equipamento.id = 0
        equipamento.id_criptografado = criptografar('0')
        form = EquipamentoForm()
        g_d = form.grupo.data
        sg_d = form.subgrupo.data
        st_d = form.setor.data
        lo_d = form.local.data
        pv_d = form.pavimento.data
        ar_d = form.und_area.data
        vo_d = form.und_volume.data
        va_d = form.und_vazao.data
        al_d = form.und_altura.data
        la_d = form.und_largura.data
        co_d = form.und_comprimento.data
        pe_d = form.und_peso.data
        po_d = form.und_potencia.data
        te_d = form.und_tensao.data

    # Listas
    grupos = Grupo.query.filter(
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Grupo.nome)

    subgrupos = Subgrupo.query.filter(
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Subgrupo.nome)

    # Listas
    setores = Setor.query.filter_by(empresa_id=current_user.empresa_id).order_by(Setor.nome)
    locais = Local.query.filter_by(empresa_id=current_user.empresa_id).order_by(Local.nome)
    pavimentos = Pavimento.query.filter_by(empresa_id=current_user.empresa_id).order_by(Pavimento.nome)

    form.setor.choices = [(0, '')] + [(st.id, st.nome) for st in setores]
    form.local.choices = [(0, '')] + [(lo.id, lo.nome) for lo in locais]
    form.pavimento.choices = [(0, '')] + [(pv.id, pv.nome) for pv in pavimentos]
    form.grupo.choices = [(0, '')] + [(g.id, g.nome) for g in grupos]
    form.subgrupo.choices = [(0, '')] + [(sg.id, sg.nome) for sg in subgrupos]
    form.und_area.choices = [(0, '')] + [(ar.id, ar.nome) for ar in Area.query.all()]
    form.und_vazao.choices = [(0, '')] + [(va.id, va.nome) for va in Vazao.query.all()]
    form.und_volume.choices = [(0, '')] + [(vol.id, vol.nome) for vol in Volume.query.all()]
    form.und_altura.choices = [(0, '')] + [(co.id, co.nome) for co in Comprimento.query.all()]
    form.und_largura.choices = [(0, '')] + [(co.id, co.nome) for co in Comprimento.query.all()]
    form.und_comprimento.choices = [(0, '')] + [(co.id, co.nome) for co in Comprimento.query.all()]
    form.und_peso.choices = [(0, '')] + [(pe.id, pe.nome) for pe in Peso.query.all()]
    form.und_potencia.choices = [(0, '')] + [(po.id, po.nome) for po in Potencia.query.all()]
    form.und_tensao.choices = [(0, '')] + [(te.id, te.nome) for te in TensaoEletrica.query.all()]

    form.grupo.data = g_d
    form.subgrupo.data = sg_d
    form.setor.data = st_d
    form.local.data = lo_d
    form.pavimento.data = pv_d
    form.und_vazao.data = va_d
    form.und_volume.data = vo_d
    form.und_area.data = ar_d
    form.und_altura.data = al_d
    form.und_largura.data = la_d
    form.und_comprimento.data = co_d
    form.und_peso.data = pe_d
    form.und_potencia.data = po_d
    form.und_tensao.data = te_d

    # Validação
    if form.validate_on_submit():
        equipamento.alterar_atributos(form, new)
        if salvar(equipamento):
            # Mensagens
            if equipamento_id > 0:
                flash("Equipamento atualizado", category="success")
            else:
                flash("Equipamento cadastrado", category="success")
            return redirect(url_for("equipamento.equipamento_listar"))
        else:
            flash("Erro no ao cadastrar/atualizar o equipamento", category="danger")
    else:
        flash_errors(form)
    return render_template("equipamento_editar.html", form=form, equipamento=equipamento,
                           grupo_id=grupo_id,
                           subgrupo_id=subgrupo_id)


@equipamento_blueprint.route('/equipamento_ativar/<equipamento_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_ativar(equipamento_id_crypto):
    # Decriptografar os ids
    equipamento_id = descriptografar(equipamento_id_crypto)

    LogsEventos.registrar("evento", equipamento_ativar.__name__, equipamento_id=equipamento_id)
    """Função para ativar um equipamento"""

    equipamento = equipamento = Equipamento.localizar_equipamento_by_id(current_user.empresa_id, equipamento_id)
    if equipamento:
        equipamento.ativar_desativar()
        if not salvar(equipamento):
            flash("Equipamento não ativado/desativado", category="danger")
    else:
        flash("Equipamento não localizado", category="danger")
    return redirect(url_for('equipamento.equipamento_listar'))


@equipamento_blueprint.route('/gerar_padrao_equipamentos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_equipamentos():
    LogsEventos.registrar("evento", gerar_padrao_equipamentos.__name__)

    csv_data = lista_para_csv([[x] for x in Equipamento.titulos_doc], None)
    nome = "tabela_base_equipamento.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"})


@equipamento_blueprint.route('/gerar_csv_equipamentos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_csv_equipamentos():
    LogsEventos.registrar("evento", gerar_csv_equipamentos.__name__)
    # Gera o arquivo csv com os titulos

    csv_data = lista_para_csv([[x] for x in Equipamento.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id
    ).all()], Equipamento.titulos_csv)

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=equipamentos.csv'}
    )


@equipamento_blueprint.route('/equipamento_excluir/<equipamento_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_excluir(equipamento_id_crypto):
    # Decriptografar os ids
    equipamento_id = descriptografar(equipamento_id_crypto)

    LogsEventos.registrar("evento", equipamento_excluir.__name__, equipamento_id=equipamento_id)

    equipamento = Equipamento.localizar_equipamento_by_id(current_user.empresa_id, equipamento_id)
    if equipamento:
        if excluir(equipamento):
            flash("Equipamento excluído", category="success")
        else:
            flash("Erro ao excluir o equipamento", category="danger")
    else:
        flash("Equipamento não cadastrado", category="danger")
    return redirect(url_for('equipamento.equipamento_listar'))


@equipamento_blueprint.route('/cadastrar_lote_equipamentos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_equipamentos():
    LogsEventos.registrar("evento", cadastrar_lote_equipamentos.__name__)

    form = EquipamentoForm()
    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Equipamento.titulos_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Equipamento.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.cod for x in Equipamento.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Subgrupo.id == Equipamento.subgrupo_id
    ).all()]

    rejeitados_texto = [['Descricao_Curta', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []

    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Descricao_Curta*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se o titulo não está no arquivo em lote
        if df.at[linha, 'Descricao_Curta*'] == 'DESCRICAO_CURTA*':
            # provavelmente é o titulo
            rejeitados.append(linha)

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Descricao_Curta*'] in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Descricao_Curta*'], "rejeitado por já existir no banco de dados"])

        # Verifica se o subgrupo existe para a empresa
        subgrupo = Subgrupo.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.nome == df.at[linha, 'Subgrupo*']).one_or_none()
        if not subgrupo:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Descricao_Curta*'], "rejeitado devido ao subgrupo não existir"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Descricao_Curta*'] in aceitos_cod:
            rejeitados.append(linha)
            rejeitados_texto.append([df.at[linha, 'Descricao_Curta*'], "rejeitado devido a estar repetido"])

        # cria um equipamento e popula ele
        equipamento = Equipamento()

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # preeche os atributos diretamente
            equipamento = preencher_objeto_atributos_semvinculo(equipamento, equipamento.titulos_valor, df, linha)
            # pesquisa os valores booleanos
            equipamento = preencher_objeto_atributos_booleanos(equipamento, equipamento.titulos_booleano, df, linha)
            # pesquisa os valores pelos objetos
            equipamento = preencher_objeto_atributos_comvinculo(equipamento, equipamento.titulos_id, df, linha)
            # verificar valores com data
            equipamento = preencher_objeto_atributos_datas(equipamento, equipamento.titulos_data, df, linha)
            # vincula a empresa no equipamento
            equipamento.subgrupo_id = subgrupo.id

            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Descricao_Curta*'])
            # insere o equipamento na lista
            aceitos.append(equipamento)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        salvar(aceitos)

    flash(f"Total de equipamentos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto) - 2}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 2:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)

        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=equipamentos_rejeitados.csv'})
    return redirect(url_for("equipamento.equipamento_listar"))


# AGRUPAMENTO ----------------------------------------------------------------------------------------

@equipamento_blueprint.route('/gerar_csv_agrupamento/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_csv_agrupamento():
    LogsEventos.registrar("evento", gerar_csv_agrupamento.__name__)

    """Função qeu gera os arquivos de csv do agrupamento"""
    # Gera o arquivo csv com os titulos
    csv_grupo = lista_para_csv([[x] for x in Grupo.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
    ).all()], Grupo.titulos_csv)
    nome_grupo = "grupos.csv"

    csv_subgrupo = lista_para_csv([[x] for x in Subgrupo.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
    ).all()], Subgrupo.titulos_csv)
    nome_subgrupo = "subgrupos.csv"

    # Criar um arquivo ZIP em memória
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(nome_grupo, csv_grupo)
        zipf.writestr(nome_subgrupo, csv_subgrupo)

    # Configurar a resposta com o arquivo ZIP
    memory_file.seek(0)
    return Response(
        memory_file,
        content_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=agrupamento.zip'}
    )


@equipamento_blueprint.route('/agrupamento_listar/<grupo_id_crypto>/<subgrupo_id_crypto>/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def agrupamento_listar(grupo_id_crypto, subgrupo_id_crypto):
    # Descriptografar os ids
    grupo_id = descriptografar(grupo_id_crypto)
    subgrupo_id = descriptografar(subgrupo_id_crypto)

    LogsEventos.registrar("evento", agrupamento_listar.__name__, grupo_id=grupo_id, subgrupo_id=subgrupo_id)

    """Função que gera a lista do agrupamento"""
    # lista de grupos existentes
    form = AgrupamentoForm()
    form_grupo = GrupoForm()
    form_subgrupo = SubgrupoForm()
    form.tipo.choices = ((0, ''), (1, 'Grupo'), (2, 'Subgrupo'))

    grupos = Grupo.query.filter(Grupo.empresa_id == current_user.empresa_id).order_by(Grupo.nome).all()
    criptografar_id_lista(grupos)
    # lista de grupos com seus quantitativos de subgrupos vinculados
    lista_grupos = [{'grupo': grupo, 'total': Subgrupo.query.filter(Subgrupo.grupo_id == grupo.id).count()}
                    for grupo in grupos]

    # lista vazia de subgrupos
    lista_subgrupos = []
    grupo = []
    subgrupo = []
    equipamentos = []

    if grupo_id > 0:
        # verifica se o grupo existe para a empresa
        grupo = Grupo.query.filter_by(id=grupo_id, empresa_id=current_user.empresa_id).one_or_none()
        if grupo:
            grupo.id_criptografado = grupo_id_crypto
            # lista de subgrupos
            subgrupos = Subgrupo.query.filter(
                Subgrupo.grupo_id == Grupo.id,
                Grupo.id == grupo_id,
                Grupo.empresa_id == current_user.empresa_id).order_by(Subgrupo.nome).all()
            criptografar_id_lista(subgrupos)
            # lista de subgrupos com o seus quantitativos de empresas vinculadas
            lista_subgrupos = [{'subgrupo': subgrupo,
                                'total': Equipamento.query.filter(Equipamento.subgrupo_id == subgrupo.id).count()}
                               for subgrupo in subgrupos]

        if subgrupo_id > 0:
            # verifica se o subgrupo existe para a empresa
            subgrupo = Subgrupo.query.filter(
                Subgrupo.id == subgrupo_id,
                Subgrupo.grupo_id == Grupo.id,
                Grupo.empresa_id == current_user.empresa_id).one_or_none()

            if subgrupo:
                # lista de equipamentos
                subgrupo.id_criptografado = criptografar(str(subgrupo.id))
                equipamentos = Equipamento.query.filter_by(subgrupo_id=subgrupo_id).order_by(
                    Equipamento.descricao_curta).all()
                criptografar_id_lista(equipamentos)

    return render_template('agrupamento_listar.html', grupo=grupo, subgrupo=subgrupo, grupos=lista_grupos,
                           subgrupos=lista_subgrupos, equipamentos=equipamentos, form=form, form_grupo=form_grupo,
                           form_subgrupo=form_subgrupo, grupo_id_crypto=grupo_id_crypto,
                           subgrupo_id_crypto=subgrupo_id_crypto)


@equipamento_blueprint.route('/agrupamento_editar/<grupo_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def agrupamento_editar(grupo_id_crypto):
    # Descriptografar os ids
    grupo_id = descriptografar(grupo_id_crypto)
    subgrupo_id_crypto = criptografar('0')

    LogsEventos.registrar("evento", agrupamento_editar.__name__, grupo_id=grupo_id)

    """Função que edita um agrupamento"""
    form = AgrupamentoForm()

    # atribui o valor do grupo no formulario
    form.grupo_id.data = grupo_id

    if form.validate_on_submit():

        # se tipo for grupo
        if form.tipo.data == 1:
            grupo = Grupo()
            grupo.alterar_atributos(form)
            salvar(grupo)
            flash("Grupo cadastrado com sucesso", category="success")
        # se tipo for subgrupo
        if form.tipo.data == 2:
            if grupo_id > 0:
                grupo = Grupo.query.filter_by(id=grupo_id, empresa_id=current_user.empresa_id).one_or_none()
                if grupo:
                    subgrupo = Subgrupo()
                    subgrupo.alterar_atributos(form, grupo_id)
                    salvar(subgrupo)
                    flash("Subgrupo cadastrado sucesso", category="success")
                else:
                    flash("Grupo não cadastrado", category="danger")
            else:
                flash("Grupo não selecionado previamente", category="danger")
    else:
        flash_errors(form)

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id_crypto=grupo_id_crypto,
                            subgrupo_id_crypto=subgrupo_id_crypto))


@equipamento_blueprint.route('/agrupamento_editar_elementos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def agrupamento_editar_elementos():
    LogsEventos.registrar("evento", agrupamento_editar_elementos.__name__)

    """Função que edita algum elemento do agrupamento"""
    # coletando as informações
    tipo = str(request.form.get('agp_tipo')).upper()

    grupo_id_crypto = request.form.get('agp_grupo_id')
    grupo_id = descriptografar(grupo_id_crypto)
    subgrupo_id_crypto = request.form.get('agp_subgrupo_id')
    subgrupo_id = descriptografar(subgrupo_id_crypto)
    tipo_nome = str(request.form.get('agp_nome')).upper()

    if tipo_nome == '':
        flash("Nome não informado", category="danger")
    else:
        if tipo == 'GRUPO':
            if grupo_id > 0:
                # valida o preenchimento
                if Grupo.query.filter(
                        current_user.empresa_id == Grupo.empresa_id,
                        Grupo.nome == tipo_nome).one_or_none():
                    flash("Já existe um grupo com este nome", category="danger")
                else:
                    # localiza a empresa do grupo
                    grupo = Grupo.query.filter(
                        current_user.empresa_id == Empresa.id,
                        Empresa.id == Grupo.empresa_id,
                        Grupo.id == grupo_id
                    ).one_or_none()
                    # se grupo existir
                    if grupo:
                        grupo.nome = tipo_nome
                        # salva no BD
                        if salvar(grupo):
                            flash("Grupo atualizado", category="success")
                        else:
                            flash("Erro ao atualizar grupo", category="danger")
                    else:
                        flash("Grupo não localizado", category="danger")
            else:
                flash("Grupo não informado", category="danger")

        if tipo == 'SUBGRUPO':
            if grupo_id > 0 and subgrupo_id > 0:
                # valida o preenchimento
                if Subgrupo.query.filter(
                        current_user.empresa_id == Grupo.empresa_id,
                        Grupo.id == Subgrupo.grupo_id,
                        Grupo.id == grupo_id,
                        Subgrupo.nome == tipo_nome).one_or_none():
                    flash("Já existe um subgrupo com este nome", category="danger")
                else:
                    # localiza a empresa do subgrupo
                    subgrupo = Subgrupo.query.filter(
                        current_user.empresa_id == Empresa.id,
                        Empresa.id == Grupo.empresa_id,
                        Grupo.id == Subgrupo.grupo_id,
                        Subgrupo.id == subgrupo_id
                    ).one_or_none()

                    # se subgrupo existir
                    if subgrupo:
                        subgrupo.nome = tipo_nome
                        # salva no BD
                        if salvar(subgrupo):
                            flash("Subgrupo atualizado", category="success")
                        else:
                            flash("Erro ao atualizar subgrupo", category="danger")
                    else:
                        flash("Subgrupo não localizado", category="danger")
            else:
                flash("Subgrupo ou Grupo não informado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id_crypto=grupo_id_crypto,
                            subgrupo_id_crypto=subgrupo_id_crypto))


@equipamento_blueprint.route('/grupo_excluir/<grupo_id_crypto>/<subgrupo_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_excluir(grupo_id_crypto, subgrupo_id_crypto):
    # Descriptografar os id
    grupo_id = descriptografar(grupo_id_crypto)
    subgrupo_id = descriptografar(subgrupo_id_crypto)

    LogsEventos.registrar("evento", grupo_excluir.__name__, grupo_id=grupo_id, subgrupo_id=subgrupo_id)

    """Função que exclui um grupo"""
    # verificar se o grupo existe
    grupo = Grupo.query.filter_by(id=grupo_id, empresa_id=current_user.empresa_id).one_or_none()

    if grupo:
        # realizar a contagem de subgrupos vinculados
        # se for >0 não permite a exclusão
        if Subgrupo.query.filter_by(grupo_id=grupo_id).count() == 0:
            if excluir(grupo):
                flash("Grupo excluído com sucesso", category="success")
            else:
                flash("Erro ao excluir o grupo", category="danger")
        else:
            flash("Não permitido excluir, pois existe subgrupo vinculado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id_crypto=grupo_id_crypto,
                            subgrupo_id_crypto=subgrupo_id_crypto))


@equipamento_blueprint.route('/subgrupo_excluir/<grupo_id_crypto>/<subgrupo_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_excluir(grupo_id_crypto, subgrupo_id_crypto):
    # Descriptografar os id
    grupo_id = descriptografar(grupo_id_crypto)
    subgrupo_id = descriptografar(subgrupo_id_crypto)

    LogsEventos.registrar("evento", subgrupo_excluir.__name__, grupo_id=grupo_id, subgrupo_id=subgrupo_id)

    """Função que exclui um subgrupo"""
    # verifica se o subgrupo existe
    subgrupo = Subgrupo.query.filter(
        Subgrupo.id == subgrupo_id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == current_user.empresa_id).one_or_none()

    if subgrupo:
        # realizar a contagem de empresas vinculadas
        # se for > 0 não permite a exclusão
        if Equipamento.query.filter_by(subgrupo_id=subgrupo_id).count() == 0:
            if excluir(subgrupo):
                flash("Subgrupo excluído com sucesso", category="success")
            else:
                flash("Erro ao excluir o subgrupo", category="danger")
        else:
            flash("Não permitido excluir, pois existe equipamento vinculado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id_crypto=grupo_id_crypto,
                            subgrupo_id_crypto=subgrupo_id_crypto))


@equipamento_blueprint.route('/gerar_padrao_agrupamento/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_agrupamento():
    LogsEventos.registrar("evento", gerar_padrao_agrupamento.__name__)

    """Função que gera o arquivo csv para o cadastro em lote"""
    csv_data = lista_para_csv([[x] for x in Subgrupo.titulos_doc], None)
    nome = "tabela_base_agrupamento.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"})


@equipamento_blueprint.route('/cadastrar_lote_agrupamento/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_agrupamento():
    LogsEventos.registrar("evento", cadastrar_lote_agrupamento.__name__)

    """Função que executa o cadastro em lote de agrupamentos"""
    form = AgrupamentoForm()

    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Subgrupo.titulos_geral_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio_grupo = [x for x in Grupo.titulos_doc if x.count('*')]
    titulos_obrigatorio_subgrupo = [x for x in Subgrupo.titulos_doc if x.count('*')]

    grupo_existente = [{'Grupo_nome': x.nome, 'Subgrupo_nome': ''}
                       for x in Grupo.query.filter(current_user.empresa_id == Grupo.empresa_id).all()]

    subgrupo_existente = [{'Grupo_nome': x.grupo.nome, 'Subgrupo_nome': x.nome}
                          for x in Subgrupo.query.filter(current_user.empresa_id == Grupo.empresa_id,
                                                         Grupo.id == Subgrupo.grupo_id).all()]

    existentes = []
    existentes.extend(grupo_existente)
    existentes.extend(subgrupo_existente)

    rejeitados_texto = [['NOME', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []

    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # verifica se os campo obrigatórios foram preenchidos
        if df.at[linha, 'Tipo*'] == "GRUPO":
            for col_ob in titulos_obrigatorio_grupo:
                # caso não seja
                if not df.at[linha, col_ob]:
                    # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Grupo_nome*'],
                         "rejeitado o grupo pelo não preenchimento de algum campo obrigatório"])

        elif df.at[linha, 'Tipo*'] == "SUBGRUPO":
            for col_ob in titulos_obrigatorio_subgrupo:
                # caso não seja
                if not df.at[linha, col_ob]:
                    # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Subgrupo_nome*'],
                         "rejeitado o subgrupo pelo não preenchimento de algum campo obrigatório"])
        else:
            rejeitados.append(linha)
            rejeitados_texto.append(
                [df.at[linha, 'Tipo*'],
                 "rejeitado pelo não preenchimento do tipo correto"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # Verifica se não existe repetições dos já salvos no BD
            grupo_nome = df.at[linha, 'Grupo_nome*']
            subgrupo_nome = df.at[linha, 'Subgrupo_nome*']

            if df.at[linha, 'Tipo*'] == "GRUPO":
                if any(grupo_nome == existente['Grupo_nome'] for existente in existentes):
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Grupo_nome*'], "rejeitado devido ao nome do grupo já existir no banco de dados"])

                if any(grupo_nome == aceito_cod['Grupo_nome'] for aceito_cod in aceitos_cod):
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Grupo_nome*'], "rejeitado devido ao nome do grupo já existir na lista"])

            if df.at[linha, 'Tipo*'] == "SUBGRUPO":
                if any(grupo_nome == existente['Grupo_nome'] and subgrupo_nome == existente['Subgrupo_nome'] for
                       existente in existentes):
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Grupo_nome*'],
                         "rejeitado devido ao nome subgrupo já existir para um grupo no banco de dados"])

                if any(grupo_nome == aceito_cod['Grupo_nome'] and subgrupo_nome == aceito_cod['Subgrupo_nome'] for
                       aceito_cod in aceitos_cod):
                    rejeitados.append(linha)
                    rejeitados_texto.append(
                        [df.at[linha, 'Grupo_nome*'], "rejeitado devido ao subgrupo já existir na lista"])

                if not Grupo.query.filter(
                        current_user.empresa_id == Empresa.id,
                        Empresa.id == Grupo.empresa_id,
                        Grupo.nome == df.at[linha, 'Grupo_nome*']).one_or_none():
                    rejeitados.append(linha)
                    rejeitados_texto.append([df.at[linha, 'Grupo_nome*'], "rejeitado devido ao grupo não existir"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            if df.at[linha, 'Tipo*'] == "GRUPO":
                grupo = Grupo()
                grupo.nome = df.at[linha, 'Grupo_nome*']
                grupo.empresa_id = current_user.empresa_id

                aceitos.append(grupo)
                # insere nas listas dos aceitos
                aceitos_cod.append({'Grupo_nome': df.at[linha, 'Grupo_nome*'], 'Subgrupo_nome': ''})

            if df.at[linha, 'Tipo*'] == "SUBGRUPO":
                subgrupo = Subgrupo()
                subgrupo.grupo_id = Grupo.query.filter(
                    current_user.empresa_id == Empresa.id,
                    Empresa.id == Grupo.empresa_id,
                    Grupo.nome == df.at[linha, 'Grupo_nome*']).one_or_none().id
                subgrupo.nome = df.at[linha, 'Subgrupo_nome*']

                aceitos.append(subgrupo)
                # insere nas listas dos aceitos
                aceitos_cod.append({'Grupo_nome': df.at[linha, 'Grupo_nome*'],
                                    'Subgrupo_nome': df.at[linha, 'Subgrupo_nome*']})

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        salvar(aceitos)

    flash(f"Total de agrupamentos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)

        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=agrupamento_rejeitados.csv'})

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=0, subgrupo_id=0))


@equipamento_blueprint.route('/subgrupo_lista/<grupo_id>', methods=['GET', 'POST'])
@login_required
def subgrupo_lista(grupo_id):
    LogsEventos.registrar("evento", subgrupo_lista.__name__, grupo_id=grupo_id)

    """    Função que retorna lista de locais"""
    subgrupos = Subgrupo.query.filter(
        current_user.empresa_id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id,
        Grupo.id == grupo_id).all()

    # com base no identificador
    subgrupoarray = []
    subgrupovazio = {'id': 0, 'nome': ''}
    subgrupoarray.append(subgrupovazio)

    for subgrupo in subgrupos:
        subgrupoobj = {'id': subgrupo.id, 'nome': subgrupo.nome}
        subgrupoarray.append(subgrupoobj)
    return jsonify({'subgrupo_lista': subgrupoarray})


# LOCALIZAÇÃO ----------------------------------------------------------------------------------------

@equipamento_blueprint.route('/localizacao_listar/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def localizacao_listar():
    LogsEventos.registrar("evento", localizacao_listar.__name__)

    """Função que retorna as listas de localização"""
    setores = Setor.query.filter_by(empresa_id=current_user.empresa_id).order_by(Setor.nome)
    locais = Local.query.filter_by(empresa_id=current_user.empresa_id).order_by(Local.nome)
    pavimentos = Pavimento.query.filter_by(empresa_id=current_user.empresa_id).order_by(Pavimento.nome)

    criptografar_id_lista(setores)
    criptografar_id_lista(locais)
    criptografar_id_lista(pavimentos)

    form = LocalizacaoForm()
    form.tipo.choices = ((0, ''), (1, 'Setor'), (2, 'Local'), (3, 'Pavimento'))
    return render_template("localizacao_listar.html", setores=setores, locais=locais, pavimentos=pavimentos,
                           form=form)


@equipamento_blueprint.route('/localizacao_editar/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def localizacao_editar():
    LogsEventos.registrar("evento", localizacao_editar.__name__)

    """Função que edita a localização"""
    form = LocalizacaoForm()

    if form.validate_on_submit():
        tipo = form.tipo.data
        models = {
            1: ('setor', Setor),
            2: ('local', Local),
            3: ('pavimento', Pavimento)
        }

        if tipo in models:
            nome, model_class = models[tipo]
            model = model_class()
            model.alterar_atributos(form)
            salvar(model)
            flash(f"Inserido o {nome} com sucesso", category="success")
        else:
            flash("Erro ao inserir pavimento", category="danger")

    return redirect(url_for('equipamento.localizacao_listar'))


@equipamento_blueprint.route('/gerar_csv_localizacao/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_csv_localizacao():
    LogsEventos.registrar("evento", gerar_csv_localizacao.__name__)

    """Função que gera o arquivo csv para o cadastro em lote de localização"""
    # Gera o arquivo csv com os titulos
    csv_setor = lista_para_csv([[x] for x in Setor.query.filter(
        current_user.empresa_id == Setor.empresa_id
    ).all()], Setor.titulos_csv)
    nome_setor = "setores.csv"

    csv_local = lista_para_csv([[x] for x in Local.query.filter(
        current_user.empresa_id == Local.empresa_id
    ).all()], Local.titulos_csv)
    nome_local = "locais.csv"

    csv_pavimento = lista_para_csv([[x] for x in Pavimento.query.filter(
        current_user.empresa_id == Pavimento.empresa_id
    ).all()], Pavimento.titulos_csv)
    nome_pavimento = "pavimentos.csv"

    # Criar um arquivo ZIP em memória
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(nome_setor, csv_setor)
        zipf.writestr(nome_local, csv_local)
        zipf.writestr(nome_pavimento, csv_pavimento)

    # Configurar a resposta com o arquivo ZIP
    memory_file.seek(0)
    return Response(
        memory_file,
        content_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=localizacao.zip'}
    )


@equipamento_blueprint.route('/cadastrar_lote_localizacao/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_localizacao():
    LogsEventos.registrar("evento", cadastrar_lote_localizacao.__name__)

    """Função que executa o cadastro em lote de localização"""
    form = LocalizacaoForm()

    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Setor.titulos_doc, encoding='latin-1'))
    # Colocar todos os valores em caixa alta
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Setor.titulos_doc if x.count('*')]

    def obter_entidades(classe, campo, filtro):
        entidades = [{'Nome': x.nome, 'Sigla': x.sigla} for x in classe.query.filter(filtro).all()]
        return entidades

    setor_existente = obter_entidades(Setor, 'nome', current_user.empresa_id == Setor.empresa_id)
    local_existente = obter_entidades(Local, 'nome', current_user.empresa_id == Local.empresa_id)
    pavimento_existente = obter_entidades(Pavimento, 'nome', current_user.empresa_id == Pavimento.empresa_id)

    existentes = []
    existentes.extend(setor_existente)
    existentes.extend(local_existente)
    existentes.extend(pavimento_existente)

    rejeitados_texto = [['NOME', 'MOTIVO']]
    rejeitados = []
    aceitos_cod = []
    aceitos = []
    # percorre por todas as linhas
    for linha in range(df.shape[0]):
        # verifica se os campo obrigatórios foram preenchidos
        for col_ob in titulos_obrigatorio:
            # caso não seja
            if not df.at[linha, col_ob]:
                # salva na lista dos rejeitados devido ao não preenchimento obrigatório
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # Verifica se não existe repetições dos já salvos no BD
            if any(df.at[linha, 'Nome*'] == existente['Nome'] for existente in existentes):
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado devido ao nome já existir no banco de dados"])

            if any(df.at[linha, 'Sigla*'] == existente['Sigla'] for existente in existentes):
                rejeitados.append(linha)
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado devido a sigla já existir no banco de dados"])

            # verifica se não existe na lista atual
            if any(df.at[linha, 'Nome*'] == aceito_cod['Nome'] for aceito_cod in aceitos_cod):
                rejeitados.append(linha)
                rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao nome estar repetido"])

            # verifica se não existe na lista atual
            if any(df.at[linha, 'Sigla*'] == aceito_cod['Sigla'] for aceito_cod in aceitos_cod):
                rejeitados.append(linha)
                rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido a sigla estar repetida"])

        # Verifica se não foi rejeitado
        if linha not in rejeitados:
            # Salvar
            tipo_classe_map = {
                "SETOR": Setor,
                "LOCAL": Local,
                "PAVIMENTO": Pavimento
            }

            tipo = df.at[linha, 'Tipo*']
            if tipo in tipo_classe_map:
                objeto = tipo_classe_map[tipo]()
                objeto.nome = df.at[linha, 'Nome*']
                objeto.sigla = df.at[linha, 'Sigla*']
                objeto.empresa_id = current_user.empresa_id
                # insere o equipamento na lista
                aceitos.append(objeto)
                # insere nas listas dos aceitos
                aceitos_cod.append({'Nome': df.at[linha, 'Nome*'], 'Sigla': df.at[linha, 'Nome*']})

    # salva a lista de localizacao no banco de dados
    if len(aceitos) > 0:
        salvar(aceitos)

    flash(f"Total de subgrupos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        csv_data = lista_para_csv(rejeitados_texto, None)
        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=localizacao_rejeitados.csv'})

    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/gerar_padrao_localizacao/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_localizacao():
    LogsEventos.registrar("evento", gerar_padrao_localizacao.__name__)

    """Função que gera o arquivo padrão para o cadastro em lote"""
    csv_data = lista_para_csv([[x] for x in Setor.titulos_doc], None)
    nome = "tabela_base_localizacao.csv"

    return Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': f"attachment; filename={nome}"})


@equipamento_blueprint.route('/setor_excluir/<setor_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def setor_excluir(setor_id_crypto):
    # descriptografar o id
    setor_id = descriptografar(setor_id_crypto)

    LogsEventos.registrar("evento", setor_excluir.__name__, setor_id=setor_id)

    """Função que exclui um setor"""
    setor = Setor.query.filter_by(id=setor_id, empresa_id=current_user.empresa_id).one_or_none()

    if setor:
        if excluir(setor):
            flash("Setor excluído", category="success")
        else:
            flash("Erro ao excluír o setor", category="danger")
    else:
        flash("Setor não cadastrado/atualizado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/local_excluir/<local_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def local_excluir(local_id_crypto):
    # descriptografar o id
    local_id = descriptografar(local_id_crypto)

    LogsEventos.registrar("evento", local_excluir.__name__, local_id=local_id)

    """Função que exclui um local"""
    local = Local.query.filter_by(id=local_id, empresa_id=current_user.empresa_id).one_or_none()

    if local:
        if excluir(local):
            flash("Local excluído", category="success")
        else:
            flash("Erro ao local o setor", category="danger")
    else:
        flash("Local não cadastrado/atualizado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/pavimento_excluir/<pavimento_id_crypto>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def pavimento_excluir(pavimento_id_crypto):
    # descriptografar o id
    pavimento_id = descriptografar(pavimento_id_crypto)

    LogsEventos.registrar("evento", pavimento_excluir.__name__, pavimento_id=pavimento_id)

    """Função que exclui um pavimento"""
    pavimento = Pavimento.query.filter_by(id=pavimento_id, empresa_id=current_user.empresa_id).one_or_none()

    if pavimento:
        if excluir(pavimento):
            flash("Pavimento excluído", category="success")
        else:
            flash("Erro ao excluir o setor", category="danger")
    else:
        flash("Pavimento não cadastrado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/localizacao_editar_elementos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def localizacao_editar_elementos():
    LogsEventos.registrar("evento", localizacao_editar_elementos.__name__)

    """Função que edita os elementos de localização"""
    # coletando as informações
    tipo = str(request.form.get('localizacao_tipo')).upper()

    tipo_id_crypto = request.form.get('localizacao_id')
    tipo_id = descriptografar(tipo_id_crypto)
    tipo_nome = str(request.form.get('localizacao_nome')).upper()
    tipo_sigla = str(request.form.get('localizacao_sigla')).upper()

    def flash_error(message):
        flash(message, category="danger")

    def flash_success(message):
        flash(message, category="success")

    def validate_and_update_location(model, model_name, tipo_id, tipo_nome, tipo_sigla):
        if tipo_id > 0:
            if model.query.filter(current_user.empresa_id == model.empresa_id,
                                  model.id != tipo_id,
                                  model.nome == tipo_nome).one_or_none():
                flash_error(f"Já existe um {model_name} com este nome")
            elif model.query.filter(model.sigla == tipo_sigla,
                                    model.id != tipo_id,
                                    model.empresa_id == current_user.empresa_id).one_or_none():
                flash_error(f"Já existe um {model_name} com esta sigla")
            else:
                location = model.query.filter(
                    current_user.empresa_id == Empresa.id,
                    Empresa.id == model.empresa_id,
                    model.id == tipo_id).one_or_none()
                if location:
                    location.nome = tipo_nome
                    location.sigla = tipo_sigla
                    if salvar(location):
                        flash_success(f"{model_name} atualizado")
                    else:
                        flash_error(f"Erro ao atualizar {model_name}")
                else:
                    flash_error(f"{model_name} não localizado")
        else:
            flash_error(f"{model_name} não informado")

    if tipo == 'SETOR':
        validate_and_update_location(Setor, 'Setor', tipo_id, tipo_nome, tipo_sigla)
    elif tipo == 'LOCAL':
        validate_and_update_location(Local, 'Local', tipo_id, tipo_nome, tipo_sigla)
    elif tipo == 'PAVIMENTO':
        validate_and_update_location(Pavimento, 'Pavimento', tipo_id, tipo_nome, tipo_sigla)
    else:
        flash_error("Tipo desconhecido")

    return redirect(url_for("equipamento.localizacao_listar"))
