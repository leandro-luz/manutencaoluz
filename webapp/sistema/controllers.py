from flask import Blueprint, redirect, url_for, render_template

sistema_blueprint = Blueprint(
    'sistema',
    __name__,
    template_folder='../templates/sistema',
    url_prefix="/sistema"
)


@sistema_blueprint.route('/')
def index():
    return render_template('sistema_home.html')

