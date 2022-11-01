from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required

sistema_blueprint = Blueprint(
    'sistema',
    __name__,
    template_folder='../templates/sistema',
    url_prefix="/sistema"
)


@sistema_blueprint.route('/')
def index():
    return render_template('sistema_home.html')


@sistema_blueprint.route('/almoxarifado', methods=['GET', 'POST'])
@login_required
def almoxarifado():
    itens = ['a', 'b', 'c', 'd']
    return render_template('almoxarifado.html', itens=itens)


@sistema_blueprint.route('/empresa', methods=['GET', 'POST'])
@login_required
def empresa():
    empresas = ['a', 'b', 'c', 'd']
    return render_template('empresa.html', empresas=empresas)


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


@sistema_blueprint.route('/manutenção', methods=['GET', 'POST'])
@login_required
def manutenção():
    ordens = ['a', 'b', 'c', 'd']
    return render_template('manutenção.html', ordens=ordens)


@sistema_blueprint.route('/orçamento', methods=['GET', 'POST'])
@login_required
def orçamento():
    custos = ['a', 'b', 'c', 'd']
    return render_template('orçamento.html', custos=custos)


@sistema_blueprint.route('/programação', methods=['GET', 'POST'])
@login_required
def programação():
    atividades = ['a', 'b', 'c', 'd']
    return render_template('programação.html', atividades=atividades)


@sistema_blueprint.route('/rh', methods=['GET', 'POST'])
@login_required
def rh():
    colaboradores = ['a', 'b', 'c', 'd']
    return render_template('rh.html', colaboradores=colaboradores)
