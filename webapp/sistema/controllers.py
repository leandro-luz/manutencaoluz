from flask import Blueprint, render_template
from flask_login import login_required

sistema_blueprint = Blueprint(
    'sistema',
    __name__,
    template_folder='../templates/sistema',
    url_prefix="/sistema"
)


@sistema_blueprint.route('/')
@login_required
def index():
    return render_template('sistema_home.html')


@sistema_blueprint.route('/almoxarifado', methods=['GET', 'POST'])
@login_required
def almoxarifado():
    itens = ['a', 'b', 'c', 'd']
    return render_template('almoxarifado.html', itens=itens)


# @sistema_blueprint.route('/empresa', methods=['GET', 'POST'])
# @login_required
# def empresa():
#     empresas = ['a', 'b', 'c', 'd']
#     return render_template('company_list.html', empresas=empresas)


@sistema_blueprint.route('/equipamento', methods=['GET', 'POST'])
@login_required
def equipamento():
    equipamentos = ['a', 'b', 'c', 'd']
    return render_template('equipamento.html', equipamentos=equipamentos)


@sistema_blueprint.route('/indicador', methods=['GET', 'POST'])
@login_required
def indicador():
    indicadores = ['a', 'b', 'c', 'd']
    return render_template('indicador.html', indicadores=indicadores)


@sistema_blueprint.route('/manutencao', methods=['GET', 'POST'])
@login_required
def manutencao():
    ordens = ['a', 'b', 'c', 'd']
    return render_template('manutencao.html', ordens=ordens)


@sistema_blueprint.route('/ferramentas', methods=['GET', 'POST'])
@login_required
def ferramentas():
    itens = ['a', 'b', 'c', 'd']
    return render_template('ferramentas.html', itens=itens)


@sistema_blueprint.route('/epi', methods=['GET', 'POST'])
@login_required
def epi():
    itens = ['a', 'b', 'c', 'd']
    return render_template('epi_epc.html', itens=itens)


@sistema_blueprint.route('/orçamento', methods=['GET', 'POST'])
@login_required
def orcamento():
    custos = ['a', 'b', 'c', 'd']
    return render_template('orcamento.html', custos=custos)


@sistema_blueprint.route('/programacao', methods=['GET', 'POST'])
@login_required
def programacao():
    atividades = ['a', 'b', 'c', 'd']
    return render_template('programacao.html', atividades=atividades)


@sistema_blueprint.route('/rh', methods=['GET', 'POST'])
@login_required
def rh():
    colaboradores = ['a', 'b', 'c', 'd']
    return render_template('rh.html', colaboradores=colaboradores)
