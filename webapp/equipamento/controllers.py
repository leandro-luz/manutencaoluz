from flask import (render_template, Blueprint, redirect, request, url_for, flash)
from flask_login import current_user, login_required
from .models import Equipamento, Grupo, Sistema
from .forms import EquipamentoForm, GrupoForm, SistemaForm
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
    equipamentos = Equipamento.query.filter_by(empresa_id=current_user.empresa_id).all()
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
            if form.grupo.data:
                g_d = form.grupo.data
            else:
                g_d = equipamento.grupo_id
        else:
            flash("Equipamento não localizado", category="danger")
            return redirect(url_for("equipamento.equipamento_listar"))
    else:
        # Cadastrar
        equipamento = Equipamento()
        equipamento.id = 0
        form = EquipamentoForm()
        g_d = form.grupo.data

    # Listas
    form.grupo.choices = [(groups.id, groups.nome) for groups in
                          Grupo.query.filter_by(empresa_id=current_user.empresa_id, ativo=True).all()]
    form.grupo.data = g_d

    form.sistema.choices = [(systems.id, systems.nome) for systems in
                            Sistema.query.filter_by(equipamento_id=equipamento.id, ativo=True).all()]

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
    for eq in total :

        for tit in Equipamento.titulos_obg:
            #verifica se o valor foi preenchido, caso contrário, ignora equipamento

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


@equipamento_blueprint.route('/grupo_listar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_listar(equipamento_id):
    grupos = Grupo.query.filter_by(empresa_id=current_user.empresa_id).filter(Grupo.nome.notlike("%None%")).all()
    return render_template('grupo_listar.html', grupos=grupos, equipamento_id=equipamento_id)


@equipamento_blueprint.route('/grupo_editar/<int:grupo_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def grupo_editar(grupo_id, equipamento_id):
    if grupo_id > 0:
        # Atualizar
        grupo = Grupo.query.filter_by(id=grupo_id).first()

        if grupo:
            form = GrupoForm(obj=grupo)
        else:
            flash("Grupo não localizado", category="danger")
            return redirect(url_for("equipamento.grupo_listar", equipamento_id=equipamento_id))
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

            return redirect(url_for("equipamento.grupo_listar", equipamento_id=equipamento_id))
        else:
            flash("Grupo não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("grupo_editar.html", form=form, grupo=grupo, equipamento_id=equipamento_id)


@equipamento_blueprint.route('/sistema_listar/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def sistema_listar(equipamento_id):
    sistemas = Sistema.query.filter_by(equipamento_id=equipamento_id).all()
    return render_template('sistema_listar.html', sistemas=sistemas, equipamento_id=equipamento_id)


@equipamento_blueprint.route('/sistema_editar/<int:sistema_id>/<int:equipamento_id>', methods=['GET', 'POST'])
@login_required
@has_view('Equipamento')
def sistema_editar(sistema_id, equipamento_id):
    if sistema_id > 0:
        # Atualizar
        sistema = Sistema.query.filter_by(id=sistema_id).first()

        if sistema:
            form = SistemaForm(obj=sistema)
        else:
            flash("Sistema não localizado", category="danger")
            return redirect(url_for("equipamento.sistema_editar", equipamento_id=equipamento_id))
    else:
        # Cadastrar
        sistema = Sistema()
        sistema.id = 0
        form = SistemaForm()

    # Validação
    if form.validate_on_submit():
        sistema.alterar_atributos(form)
        sistema.equipamento_id = equipamento_id
        if sistema.salvar():
            # Mensagens
            if sistema_id > 0:
                flash("Sistema atualizado", category="success")
            else:
                flash("Sistema cadastrado", category="success")
            return redirect(url_for("equipamento.sistema_listar", equipamento_id=equipamento_id))
        else:
            flash("Sistema não cadastrado/atualizado", category="danger")
    else:
        flash_errors(form)
    return render_template("sistema_editar.html", form=form, sistema=sistema, sistema_id=sistema_id, equipamento_id=equipamento_id)
