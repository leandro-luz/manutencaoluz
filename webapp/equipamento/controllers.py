from flask import (render_template, Blueprint, redirect, request, url_for, flash)
from flask_login import current_user, login_required
from webapp.empresa.models import Empresa
from .models import Equipamento, Grupo, Subgrupo
from .forms import EquipamentoForm, GrupoForm, SubgrupoForm
from werkzeug.utils import secure_filename
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
        Equipamento.descricao_curta)
    return render_template('equipamento_listar.html', equipamentos=equipamentos)


@equipamento_blueprint.route('/equipamento_editar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def equipamento_editar(equipamento_id):
    if equipamento_id > 0:
        # Atualizar
        equipamento = Equipamento.query.filter_by(id=equipamento_id).one_or_none()

        if equipamento:
            form = EquipamentoForm(obj=equipamento)
            # Atualizar ou Ler dados
            if form.subgrupo.data:
                sg_d = form.subgrupo.data
            else:
                sg_d = equipamento.subgrupo_id
        else:
            flash("Equipamento não localizado", category="danger")
            return redirect(url_for("equipamento.equipamento_listar"))
    else:
        # Cadastrar
        equipamento = Equipamento()
        equipamento.id = 0
        form = EquipamentoForm()
        sg_d = form.subgrupo.data

    # Listas
    subgrupos = Subgrupo.query.filter(
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Subgrupo.nome)
    form.subgrupo.choices = [(0, '')] + [(sg.id, sg.nome) for sg in subgrupos]
    form.subgrupo.data = sg_d

    # Validação
    if form.validate_on_submit():
        equipamento.alterar_atributos(form)
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
    return render_template("equipamento_editar.html", form=form, equipamento=equipamento)


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
    result, path = arquivo_padrao(nome_arquivo=Equipamento.nome_doc, titulos=Equipamento.titulos_doc)
    if result:
        flash(f'Foi gerado o arquivo padrão no caminho: {path}', category="success")
    else:
        flash("Não foi gerado o arquivo padrão", category="dander")
    return redirect(url_for("equipamento.equipamento_listar"))


@equipamento_blueprint.route('/cadastrar_lote_equipamentos/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def cadastrar_lote_equipamentos(equipamento_id):
    import pandas as pd

    form = EquipamentoForm()
    # file = request.files['arquivo']

    filename = secure_filename(form.file.data.filename)
    filestream = form.file.data
    filestream.seek(0)
    df = pd.DataFrame(pd.read_csv(filestream, sep=";", names=Equipamento.titulos_doc, encoding='latin-1'))

    # total de linhas
    total = int(len(df[df.columns[0]].count()))
    # percorre pelos titulos obrigatórios
    for eq in total:

        for tit in Equipamento.titulos_obg:
            # verifica se o valor foi preenchido, caso contrário, ignora equipamento

            print(tit)

    # if file:
    #     df = pd.read_excel(files_excel["file"])

    # csv = pd.read_csv(filename, sep=',', encoding='latin-1')
    #
    # print(csv.info())

    # print(file)
    # from csv import reader
    # with open(filename) as f:
    #     leitor_csv = reader(f)
    #     # reader = csv.reader(f)
    #     for linha in leitor_csv:
    #         print(linha)

    #
    # if 'file' not in request.files:
    #     print("b")
    #     flash("Não tem a parte do arquivo", category="danger")
    #     return redirect(url_for("equipamento.equipamento_editar", equipamento_id=equipamento_id))
    # file = request.files['arquivo']
    #
    # print("c")
    #
    # # se o usuário não enviar o arquivo o navegador envia um arquivo vazio sem o nome
    # if file.filename == '':
    #     print("d")
    #     flash("Nenhum arquivo selecionado")
    #     return redirect(url_for("equipamento.equipamento_editar", equipamento_id=equipamento_id))
    # # if file and allowed_file(file.filename):
    #
    # print("e")
    # filename = secure_filename(file.filename)
    # print(filename)
    #
    # print("f")
    # print('entrada da lista para o cadastro de equipamentos em lote')
    #
    # # file = request.files['file']
    # # print(file.razao_social)
    # # print(file.headers)
    # print("g")
    return redirect(url_for("equipamento.equipamento_listar"))


@equipamento_blueprint.route('/grupo_listar/<int:subgrupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_listar(subgrupo_id, equipamento_id):
    grupos = Grupo.query.filter(
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Grupo.nome)
    return render_template('grupo_listar.html', grupos=grupos, subgrupo_id=subgrupo_id, equipamento_id=equipamento_id)


@equipamento_blueprint.route('/grupo_editar/<int:grupo_id>/<int:subgrupo_id>/<int:equipamento_id>',
                             methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_editar(grupo_id, subgrupo_id, equipamento_id):
    if grupo_id > 0:
        # Atualizar
        grupo = Grupo.query.filter_by(id=grupo_id).first()

        if grupo:
            form = GrupoForm(obj=grupo)
        else:
            flash("Grupo não localizado", category="danger")
            return redirect(url_for("equipamento.grupo_listar", subgrupo_id=subgrupo_id, equipamento_id=equipamento_id))
    else:
        # Cadastrar
        grupo = Grupo()
        grupo.id = 0
        form = GrupoForm()

    # Validação
    if form.validate_on_submit():
        grupo.alterar_atributos(form)
        if grupo.salvar():
            # Mensagens
            if grupo_id > 0:
                flash("Grupo atualizado", category="success")
            else:
                flash("Grupo cadastrado", category="success")

            return redirect(url_for("equipamento.grupo_listar", subgrupo_id=subgrupo_id, equipamento_id=equipamento_id))
        else:
            flash("Grupo não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("grupo_editar.html", form=form, grupo=grupo, subgrupo_id=subgrupo_id,
                           equipamento_id=equipamento_id)


@equipamento_blueprint.route('/grupo_ativar/<int:grupo_id>//<int:subgrupo_id>//<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_ativar(grupo_id, subgrupo_id, equipamento_id):
    """    Função que ativa/desativa um grupo    """
    # instância um grupo com base no identificador
    grupo = Grupo.query.filter_by(id=grupo_id).one_or_none()
    # se o grupo existir
    if grupo:
        # ativa/inativa o grupo
        grupo.ativar_desativar()
        # salva no banco de dados a alteração
        if grupo.salvar():
            flash("Grupo ativado/desativado com sucesso", category="success")
        else:
            flash("Grupo não foi ativado/desativado", category="danger")
    else:
        flash("Grupo não registrado", category="danger")
    return redirect(url_for('equipamento.grupo_listar', subgrupo_id=subgrupo_id, equipamento_id=equipamento_id))


@equipamento_blueprint.route('/subgrupo_ativar/<int:subgrupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_ativar(subgrupo_id, equipamento_id):
    """    Função que ativa/desativa um subgrupo    """
    # instância um subgrupo com base no identificador
    subgrupo = Subgrupo.query.filter_by(id=subgrupo_id).one_or_none()
    # se o subgrupo existir
    if subgrupo:
        # ativa/inativa o subgrupo
        subgrupo.ativar_desativar()
        # salva no banco de dados a alteração
        if subgrupo.salvar():
            flash("Subgrupo ativado/desativado com sucesso", category="success")
        else:
            flash("Subgrupo não foi ativado/desativado", category="danger")
    else:
        flash("Subgrupo não registrado", category="danger")
    return redirect(url_for("equipamento.subgrupo_listar", equipamento_id=equipamento_id))


@equipamento_blueprint.route('/subgrupo_listar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_listar(equipamento_id):
    subgrupos = Subgrupo.query.filter(
        Subgrupo.grupo_id == Grupo.id,
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).order_by(
        Subgrupo.nome)
    return render_template('subgrupo_listar.html', subgrupos=subgrupos, equipamento_id=equipamento_id)


@equipamento_blueprint.route('/subgrupo_editar/<int:subgrupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def subgrupo_editar(subgrupo_id, equipamento_id):
    if subgrupo_id > 0:
        # Atualizar
        subgrupo = Subgrupo.query.filter_by(id=subgrupo_id).first()

        if subgrupo:
            form = SubgrupoForm(obj=subgrupo)

            if form.grupo.data:
                g_d = form.grupo.data
            else:
                g_d = subgrupo.grupo_id

        else:
            flash("Subgrupo não localizado", category="danger")
            return redirect(url_for("equipamento.subgrupo_editar", equipamento_id=equipamento_id))
    else:
        # Cadastrar
        subgrupo = Subgrupo()
        subgrupo.id = 0
        form = SubgrupoForm()
        g_d = form.grupo.data

    # Lista
    grupos = Grupo.query.filter(
        Grupo.empresa_id == Empresa.id,
        Empresa.id == current_user.empresa_id).all()
    form.grupo.choices = [(0, '')] + [(sg.id, sg.nome) for sg in grupos]
    form.grupo.data = g_d

    # Validação
    if form.validate_on_submit():
        subgrupo.alterar_atributos(form)
        subgrupo.equipamento_id = equipamento_id
        if subgrupo.salvar():
            # Mensagens
            if subgrupo_id > 0:
                flash("Subgrupo atualizado", category="success")
            else:
                flash("Subgrupo cadastrado", category="success")
            return redirect(url_for("equipamento.subgrupo_listar", equipamento_id=equipamento_id))
        else:
            flash("Subgrupo não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("subgrupo_editar.html", form=form, subgrupo=subgrupo, subgrupo_id=subgrupo_id,
                           equipamento_id=equipamento_id)
