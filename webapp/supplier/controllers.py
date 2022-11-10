from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import login_user, logout_user, current_user, login_required
# from .models import db, Asset
from webapp.company.models import Company
from webapp.email import send_email

# from .forms import LoginForm, RegisterForm, ChangePasswordForm, \
#     PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

supplier_blueprint = Blueprint(
    'supplier',
    __name__,
    template_folder='../templates/sistema/supplier',
    url_prefix="/fornecedor"
)
