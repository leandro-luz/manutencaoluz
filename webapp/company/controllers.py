from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_required

company_blueprint = Blueprint(
    'company',
    __name__,
    template_folder='../templates/sistema/company',
    url_prefix="/sistema"
)


@company_blueprint.route('/company_list', methods=['GET', 'POST'])
@login_required
def list():
    empresas = ['a', 'b', 'c', 'd']

    return render_template('list.html', empresas=empresas)
