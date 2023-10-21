import numpy as np
import pandas as pd
from flask import render_template, Blueprint, redirect, url_for, flash, Response
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from .models import Equipamento, Grupo, Subgrupo, Pavimento, Setor, Local, Area, Volume, Vazao, Comprimento, Peso, \
    Potencia, TensaoEletrica
from .forms import EquipamentoForm, GrupoForm, SubgrupoForm, LocalizacaoForm, AgrupamentoForm, SetorForm, LocalForm, \
    PavimentoForm
from webapp.usuario import has_view
from webapp.utils.files import arquivo_padrao
from webapp.utils.erros import flash_errors

equipamento_blueprint = Blueprint(
    'equipamento',
    __name__,
    template_folder='../templates/sistema/equipamento',
    url_prefix="/sistema"
)


@equipamento_blueprint.route('/equipamento_listar', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_listar():
    """Retorna a lista de equipamentos"""
    equipamentos = Equipamento.query.filter(
        Equipamento.subgrupo_id == Subgrupo.id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Equipamento.cod)
    return render_template('equipamento_listar.html', equipamentos=equipamentos)


@equipamento_blueprint.route('/equipamento_editar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_editar(equipamento_id):
    grupo_id = 0
    subgrupo_id = 0
    new = True

    if equipamento_id > 0:
        # Atualizar
        # localiza a empresa do equipamento
        new = False

        equipamento = Equipamento.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == Equipamento.subgrupo_id,
            Equipamento.id == equipamento_id
        ).one_or_none()

        # verifica se o equipamento existe e se pertence a empresa do usuário
        if equipamento:
            form = EquipamentoForm(obj=equipamento)
            grupo_id = equipamento.subgrupo.grupo_id
            subgrupo_id = equipamento.subgrupo_id
            # Atualizar ou Ler dados
            if form.subgrupo.data:
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
        equipamento = Equipamento()
        equipamento.id = 0
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
    setores = Setor.query.filter_by(
        empresa_id=current_user.empresa_id).order_by(Setor.nome)

    locais = Local.query.filter_by(
        empresa_id=current_user.empresa_id).order_by(Local.nome)

    pavimentos = Pavimento.query.filter_by(
        empresa_id=current_user.empresa_id).order_by(Pavimento.nome)

    form.setor.choices = [(0, '')] + [(st.id, st.nome) for st in setores]
    form.local.choices = [(0, '')] + [(lo.id, lo.nome) for lo in locais]
    form.pavimento.choices = [(0, '')] + [(pv.id, pv.nome) for pv in pavimentos]
    form.grupo.choices = [(0, '')] + [(g.id, g.nome) for g in grupos]
    form.subgrupo.choices = [(0, '')] + [(sg.id, sg.nome) for sg in subgrupos]
    form.und_area.choices = [(0, '')] + [(ar.id, ar.unidade) for ar in Area.query.all()]
    form.und_vazao.choices = [(0, '')] + [(va.id, va.unidade) for va in Vazao.query.all()]
    form.und_volume.choices = [(0, '')] + [(vol.id, vol.unidade) for vol in Volume.query.all()]
    form.und_altura.choices = [(0, '')] + [(co.id, co.unidade) for co in Comprimento.query.all()]
    form.und_largura.choices = [(0, '')] + [(co.id, co.unidade) for co in Comprimento.query.all()]
    form.und_comprimento.choices = [(0, '')] + [(co.id, co.unidade) for co in Comprimento.query.all()]
    form.und_peso.choices = [(0, '')] + [(pe.id, pe.unidade) for pe in Peso.query.all()]
    form.und_potencia.choices = [(0, '')] + [(po.id, po.unidade) for po in Potencia.query.all()]
    form.und_tensao.choices = [(0, '')] + [(te.id, te.unidade) for te in TensaoEletrica.query.all()]

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
        if equipamento.salvar():
            # Mensagens
            if equipamento_id > 0:
                flash("Equipamento atualizado", category="success")
            else:
                flash("Equipamento cadastrado", category="success")
            return redirect(url_for("equipamento.equipamento_listar"))
        else:
            flash("Equipamento não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("equipamento_editar.html", form=form, equipamento=equipamento, grupo_id=grupo_id,
                           subgrupo_id=subgrupo_id)


@equipamento_blueprint.route('/equipamento_ativar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_ativar(equipamento_id):
    equipamento = Equipamento.query.filter_by(id=equipamento_id).one_or_none()
    if equipamento:
        equipamento.ativar_desativar()
        if not equipamento.salvar():
            flash("Equipamento não ativado/desativado", category="danger")
    else:
        flash("Equipamento não localizado", category="danger")
    return redirect(url_for('equipamento.equipamento_listar'))


@equipamento_blueprint.route('/gerar_padrao_equipamentos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_equipamentos():
    result, path = arquivo_padrao(nome_arquivo=Equipamento.nome_doc, valores=[[x] for x in Equipamento.titulos_doc])
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
    else:
        flash("Não foi gerado o arquivo padrão", category="danger")
    return redirect(url_for("equipamento.equipamento_listar"))


@equipamento_blueprint.route('/cadastrar_lote_equipamentos/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_equipamentos():
    form = EquipamentoForm()

    # filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Equipamento.titulos_doc, encoding='latin-1'))

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

    rejeitados_texto = [['CÓDIGO', 'MOTIVO']]
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
                rejeitados.append(df.at[linha, 'Código*'])
                rejeitados_texto.append(
                    [df.at[linha, 'Código*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Código*'].upper() in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado por já existir no banco de dados"])

        # Verifica se o subgrupo existe para a empresa
        subgrupo = Subgrupo.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.nome == df.at[linha, 'Subgrupo*'].upper()).one_or_none()
        if not subgrupo:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido ao subgrupo não existir"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Código*'] in aceitos_cod:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if df.at[linha, 'Código*'] not in rejeitados:
            # altera o valor do subgrupo de nome para id na tabela
            df.at[linha, 'Subgrupo*'] = subgrupo.id

            # cria um equipamento e popula ele
            equipamento = Equipamento()
            for k, v in equipamento.titulos_doc.items():
                # recupere o valor
                valor = df.at[linha, k]
                if str(valor).isnumeric() or valor is None:
                    # Salva o atributo se o valor e numerico ou nulo
                    setattr(equipamento, v, valor)
                else:
                    # Salva o atributo quando texto
                    setattr(equipamento, v, valor.upper())

            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Código*'])
            # insere o equipamento na lista
            aceitos.append(equipamento)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        Equipamento.salvar_lote(aceitos)

    flash(f"Total de equipamentos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        result, path = arquivo_padrao(nome_arquivo="Equipamentos_rejeitados", valores=rejeitados_texto)
        if result:
            flash(f'Foi gerado o arquivo de equipamentos rejeitados no caminho: {path}', category="warning")
        else:
            flash("Não foi gerado o arquivo de equipamentos rejeitados", category="danger")

    return redirect(url_for("equipamento.equipamento_listar"))


@equipamento_blueprint.route('/agrupamento_listar/<int:grupo_id>/<int:subgrupo_id>/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def agrupamento_listar(grupo_id, subgrupo_id):
    # lista de grupos existentes

    form = AgrupamentoForm()
    form_grupo = GrupoForm()
    form_subgrupo = SubgrupoForm()
    form.tipo.choices = ((0, ''), (1, 'Grupo'), (2, 'Subgrupo'))

    grupos = Grupo.query.filter(
        Grupo.empresa_id == current_user.empresa_id).order_by(Grupo.nome).all()
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
            # lista de subgrupos
            subgrupos = Subgrupo.query.filter(
                Subgrupo.grupo_id == Grupo.id,
                Grupo.id == grupo_id,
                Grupo.empresa_id == current_user.empresa_id).order_by(Subgrupo.nome).all()
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
                equipamentos = Equipamento.query.filter_by(subgrupo_id=subgrupo_id).order_by(
                    Equipamento.descricao_curta).all()

    return render_template('agrupamento_listar.html', grupo=grupo, subgrupo=subgrupo, grupos=lista_grupos,
                           subgrupos=lista_subgrupos, equipamentos=equipamentos, form=form, form_grupo=form_grupo,
                           form_subgrupo=form_subgrupo, grupo_id=grupo_id, subgrupo_id=subgrupo_id)


@equipamento_blueprint.route('/agrupamento_editar/<int:grupo_id>/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def agrupamento_editar(grupo_id):
    form = AgrupamentoForm()

    if form.validate_on_submit():

        # se tipo for grupo
        if form.tipo.data == 1:
            grupo = Grupo()
            grupo.alterar_atributos(form)
            grupo.salvar()
            flash("Grupo cadastrado com sucesso", category="success")
        # se tipo for subgrupo
        if form.tipo.data == 2:
            if grupo_id > 0:
                grupo = Grupo.query.filter_by(id=grupo_id, empresa_id=current_user.empresa_id).one_or_none()
                if grupo:
                    subgrupo = Subgrupo()
                    subgrupo.alterar_atributos(form, grupo_id)
                    subgrupo.salvar()
                    flash("Subgrupo cadastrado sucesso", category="success")
                else:
                    flash("Grupo não cadastrado", category="danger")
            else:
                flash("Grupo não selecionado previamente", category="danger")
    else:
        flash_errors(form)

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=grupo_id, subgrupo_id=0))


@equipamento_blueprint.route('/grupo_excluir/<int:grupo_id>/<int:subgrupo_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_excluir(grupo_id, subgrupo_id):
    # verificar se o grupo existe
    grupo = Grupo.query.filter_by(id=grupo_id, empresa_id=current_user.empresa_id).one_or_none()

    if grupo:
        # realizar a contagem de subgrupos vinculados
        # se for >0 não permite a exclusão
        if Subgrupo.query.filter_by(grupo_id=grupo_id).count() == 0:
            if grupo.excluir():
                flash("Grupo excluído com sucesso", category="success")
            else:
                flash("Erro ao excluir o grupo", category="danger")
        else:
            flash("Não permitido excluir, pois existe subgrupo vinculado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=grupo_id, subgrupo_id=subgrupo_id))


@equipamento_blueprint.route('/grupo_editar/<int:grupo_id>/<int:subgrupo_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_editar(grupo_id, subgrupo_id):
    if grupo_id > 0:
        # localiza a empresa do grupo
        grupo = Grupo.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == grupo_id
        ).one_or_none()

        # se grupo existir
        if grupo:
            form = GrupoForm(obj=grupo)
            # Validação
            if form.validate_on_submit():
                grupo.alterar_atributos(form)
                if grupo.salvar():
                    flash("Grupo atualizado", category="success")
                else:
                    flash("Erro ao atualizar grupo", category="danger")
            else:
                flash_errors(form)
        else:
            flash("Grupo não localizado", category="danger")
    else:
        flash("Grupo não informado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=grupo_id, subgrupo_id=subgrupo_id))


@equipamento_blueprint.route('/subgrupo_excluir/<int:grupo_id>/<int:subgrupo_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_excluir(grupo_id, subgrupo_id):
    # verifica se o subgrupo existe
    subgrupo = Subgrupo.query.filter(
        Subgrupo.id == subgrupo_id,
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == current_user.empresa_id).one_or_none()

    if subgrupo:
        # realizar a contagem de empresas vinculadas
        # se for > 0 não permite a exclusão
        if Equipamento.query.filter_by(subgrupo_id=subgrupo_id).count() == 0:
            if subgrupo.excluir():
                flash("Subgrupo excluído com sucesso", category="success")
            else:
                flash("Erro ao excluir o subgrupo", category="danger")
        else:
            flash("Não permitido excluir, pois existe equipamento vinculado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=grupo_id, subgrupo_id=subgrupo_id))


@equipamento_blueprint.route('/gerar_padrao_grupos/<int:subgrupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_grupos(subgrupo_id, equipamento_id):
    resultado, nome, arquivo = arquivo_padrao(nome_arquivo=Grupo.nome_doc, valores=[[x] for x in Grupo.titulos_doc])

    # se não houver erro envia o arquivo
    if resultado:
        return Response(arquivo, mimetype="text/csv",
                        headers={"Content-disposition": f"attachment; filename={nome}"})


@equipamento_blueprint.route('/cadastrar_lote_grupos/<int:subgrupo_id>/<int:equipamento_id>>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_grupos(subgrupo_id, equipamento_id):
    form = GrupoForm()

    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Grupo.titulos_doc, encoding='latin-1'))

    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Grupo.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.nome for x in Grupo.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id
    ).all()]

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
                rejeitados.append(df.at[linha, 'Código*'])
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])

        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Nome*'].upper() in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado por já existir no banco de dados"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Nome*'] in aceitos_cod:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Código*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if df.at[linha, 'Nome*'] not in rejeitados:
            # cria um equipamento e popula ele
            grupo = Grupo()
            grupo.nome = df.at[linha, 'Nome*'].upper()
            grupo.empresa_id = current_user.empresa_id
            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Nome*'])
            # insere o equipamento na lista
            aceitos.append(grupo)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        Grupo.salvar_lote(aceitos)

    flash(f"Total de grupos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        result, path = arquivo_padrao(nome_arquivo="Grupos_rejeitados", valores=rejeitados_texto)
        if result:
            flash(f'Foi gerado o arquivo de grupos rejeitados no caminho: {path}', category="warning")
        else:
            flash("Não foi gerado o arquivo de grupos rejeitados", category="danger")

    return redirect(url_for('equipamento.grupo_listar', subgrupo_id=subgrupo_id, equipamento_id=equipamento_id))


@equipamento_blueprint.route('/subgrupo_editar/<int:grupo_id>/<int:subgrupo_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_editar(grupo_id, subgrupo_id):
    if subgrupo_id > 0:
        # localiza a empresa do grupo
        subgrupo = Subgrupo.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.id == Subgrupo.grupo_id,
            Subgrupo.id == subgrupo_id
        ).one_or_none()

        # se grupo existir
        if subgrupo:
            form = SubgrupoForm(obj=subgrupo)
            # Validação
            if form.validate_on_submit():
                subgrupo.alterar_atributos(form, grupo_id)
                if subgrupo.salvar():
                    flash("Subgrupo atualizado", category="success")
                else:
                    flash("Erro ao atualizar subgrupo", category="danger")
            else:
                flash_errors(form)
        else:
            flash("Subgrupo não localizado", category="danger")
    else:
        flash("Subgrupo não informado", category="danger")

    return redirect(url_for("equipamento.agrupamento_listar", grupo_id=grupo_id, subgrupo_id=subgrupo_id))


@equipamento_blueprint.route('/gerar_padrao_subgrupos/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def gerar_padrao_subgrupos(equipamento_id):
    result, path = arquivo_padrao(nome_arquivo=Subgrupo.nome_doc, valores=[[x] for x in Subgrupo.titulos_doc])
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
    else:
        flash("Não foi gerado o arquivo padrão", category="danger")
    return redirect(url_for('equipamento.subgrupo_listar', equipamento_id=equipamento_id))


@equipamento_blueprint.route('/cadastrar_lote_subgrupos>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_subgrupos(equipamento_id):
    form = SubgrupoForm()

    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Subgrupo.titulos_doc, encoding='latin-1'))

    # converter os valores Nan para Null
    df = df.replace({np.NAN: None})

    # lista dos titulos obrigatórios
    titulos_obrigatorio = [x for x in Subgrupo.titulos_doc if x.count('*')]
    # lista dos equipamentos existentes
    existentes = [x.nome for x in Subgrupo.query.filter(
        current_user.empresa_id == Empresa.id,
        Empresa.id == Grupo.empresa_id,
        Grupo.id == Subgrupo.grupo_id
    ).all()]

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
                rejeitados.append(df.at[linha, 'Código*'])
                rejeitados_texto.append(
                    [df.at[linha, 'Nome*'], "rejeitado pelo não preenchimento de algum campo obrigatório"])
        # Verifica se não existe repetições dos já salvos no BD
        if df.at[linha, 'Nome*'].upper() in existentes:
            # salva na lista dos rejeitados devido a repetição
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado por já existir no banco de dados"])

        # Verifica se o grupo existe para a empresa
        grupo = Grupo.query.filter(
            current_user.empresa_id == Empresa.id,
            Empresa.id == Grupo.empresa_id,
            Grupo.nome == df.at[linha, 'Grupo*'].upper()).one_or_none()
        if not grupo:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido ao grupo não existir"])

        # verifica se não existe na lista atual
        if df.at[linha, 'Nome*'] in aceitos_cod:
            rejeitados.append(df.at[linha, 'Código*'])
            rejeitados_texto.append([df.at[linha, 'Nome*'], "rejeitado devido a estar repetido"])

        # Verifica se não foi rejeitado
        if df.at[linha, 'Nome*'] not in rejeitados:
            # cria um subgrupo e popula ele
            subgrupo = Subgrupo()
            subgrupo.nome = df.at[linha, 'Nome*'].upper()
            subgrupo.grupo_id = grupo.id

            # insere nas listas dos aceitos
            aceitos_cod.append(df.at[linha, 'Nome*'])
            # insere o equipamento na lista
            aceitos.append(subgrupo)

    # salva a lista de equipamentos no banco de dados
    if len(aceitos) > 0:
        Subgrupo.salvar_lote(aceitos)

    flash(f"Total de subgrupos cadastrados: {len(aceitos)}, rejeitados:{len(rejeitados_texto)}", "success")

    # se a lista de rejeitados existir
    if len(rejeitados_texto) > 0:
        # publica ao usuário a lista dos rejeitados
        result, path = arquivo_padrao(nome_arquivo="Subgrupos_rejeitados", valores=rejeitados_texto)
        if result:
            flash(f'Foi gerado o arquivo de subgrupos rejeitados no caminho: {path}', category="warning")
        else:
            flash("Não foi gerado o arquivo de subgrupos rejeitados", category="danger")

    return redirect(url_for('equipamento.subgrupo_listar', equipamento_id=equipamento_id))


@equipamento_blueprint.route('/localizacao_listar/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def localizacao_listar():
    setores = Setor.query.filter_by(empresa_id=current_user.empresa_id).order_by(Setor.nome)
    locais = Local.query.filter_by(empresa_id=current_user.empresa_id).order_by(Local.nome)
    pavimentos = Pavimento.query.filter_by(empresa_id=current_user.empresa_id).order_by(Pavimento.nome)

    form = LocalizacaoForm()
    form_setor = SetorForm()
    form_local = LocalForm()
    form_pavimento = PavimentoForm()
    form.tipo.choices = ((0, ''), (1, 'Setor'), (2, 'Local'), (3, 'Pavimento'))
    return render_template("localizacao_listar.html", setores=setores, locais=locais, pavimentos=pavimentos,
                           form=form, form_setor=form_setor, form_local=form_local, form_pavimento=form_pavimento)


@equipamento_blueprint.route('/localizacao_editar/', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def localizacao_editar():
    form = LocalizacaoForm()

    if form.validate_on_submit():
        if form.tipo.data == 1:
            nome = 'setor'
            setor = Setor()
            setor.alterar_atributos(form)
            setor.salvar()
        elif form.tipo.data == 2:
            nome = 'local'
            local = Local()
            local.alterar_atributos(form)
            local.salvar()
        elif form.tipo.data == 3:
            nome = 'pavimento'
            pavimento = Pavimento()
            pavimento.alterar_atributos(form)
            pavimento.salvar()
        else:
            flash("Erro ao inserir pavimento", category="danger")
            return redirect(url_for('equipamento.localizacao_listar'))
        flash(f"Inserido o {nome} com sucesso", category="success")
    else:
        flash_errors(form)

    return redirect(url_for('equipamento.localizacao_listar'))


@equipamento_blueprint.route('/setor_excluir/<int:setor_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def setor_excluir(setor_id):
    setor = Setor.query.filter_by(id=setor_id, empresa_id=current_user.empresa_id).one_or_none()

    if setor:
        if setor.excluir():
            flash("Setor excluído", category="success")
        else:
            flash("Erro ao excluír o setor", category="danger")
    else:
        flash("Setor não cadastrado/atualizado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/setor_editar/<int:setor_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def setor_editar(setor_id):
    if setor_id > 0:
        # localiza a empresa do grupo
        setor = Setor.query.filter(
            current_user.empresa_id == Setor.empresa_id,
            Setor.id == setor_id
        ).one_or_none()

        # se setor existir
        if setor:
            form = SetorForm(obj=setor)
            # Validação
            if form.validate_on_submit():
                setor.alterar_atributos(form)
                if setor.salvar():
                    flash("Setor atualizado", category="success")
                else:
                    flash("Erro ao atualizar setor", category="danger")
            else:
                flash_errors(form)
        else:
            flash("Setor não localizado", category="danger")
    else:
        flash("Setor não informado", category="danger")

    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/local_excluir/<int:local_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def local_excluir(local_id):
    local = Local.query.filter_by(id=local_id, empresa_id=current_user.empresa_id).one_or_none()

    if local:
        if local.excluir():
            flash("Local excluído", category="success")
        else:
            flash("Erro ao local o setor", category="danger")
    else:
        flash("Local não cadastrado/atualizado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/local_editar/<int:local_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def local_editar(local_id):
    if local_id > 0:
        # localiza a empresa do grupo
        local = Local.query.filter(
            current_user.empresa_id == Local.empresa_id,
            Local.id == local_id
        ).one_or_none()

        # se local existir
        if local:
            form = LocalForm(obj=local)
            # Validação
            if form.validate_on_submit():
                local.alterar_atributos(form)
                if local.salvar():
                    flash("Local atualizado", category="success")
                else:
                    flash("Erro ao atualizar setor", category="danger")
            else:
                flash_errors(form)
        else:
            flash("Local não localizado", category="danger")
    else:
        flash("Local não informado", category="danger")

    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/pavimento_excluir/<int:pavimento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def pavimento_excluir(pavimento_id):
    pavimento = Pavimento.query.filter_by(id=pavimento_id, empresa_id=current_user.empresa_id).one_or_none()

    if pavimento:
        if pavimento.excluir():
            flash("Pavimento excluído", category="success")
        else:
            flash("Erro ao setor o setor", category="danger")
    else:
        flash("Pavimento não cadastrado/atualizado", category="danger")
    return redirect(url_for("equipamento.localizacao_listar"))


@equipamento_blueprint.route('/pavimento_editar/<int:pavimento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def pavimento_editar(pavimento_id):
    if pavimento_id > 0:
        # localiza a empresa do grupo
        pavimento = Pavimento.query.filter(
            current_user.empresa_id == Pavimento.empresa_id,
            Pavimento.id == pavimento_id
        ).one_or_none()

        # se pavimento existir
        if pavimento:
            form = PavimentoForm(obj=pavimento)
            # Validação
            if form.validate_on_submit():
                pavimento.alterar_atributos(form)
                if pavimento.salvar():
                    flash("Pavimento atualizado", category="success")
                else:
                    flash("Erro ao atualizar pavimento", category="danger")
            else:
                flash_errors(form)
        else:
            flash("Pavimento não localizado", category="danger")
    else:
        flash("Pavimento não informado", category="danger")

    return redirect(url_for("equipamento.localizacao_listar"))
