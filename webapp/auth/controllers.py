from flask import (render_template,
                   Blueprint,
                   redirect,
                   request,
                   url_for,
                   flash)
from flask_login import login_user, logout_user, current_user, login_required
from webapp.auth.models import db, User
from webapp.email import send_email
from .forms import LoginForm, RegisterForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        if user.confirmed:
            login_user(user, remember=form.remember.data)
            user.ping()
            flash("Você está dentro do sistema.", category="success")
            return redirect(url_for('sistema.index'))
        return render_template('unconfirmed.html', user=user)
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", category="success")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data.lower())
        new_user.set_email(form.email.data.lower())
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.create_token("confirm")
        send_email(new_user.email,
                   'Confirmação de Conta',
                   'auth/email/confirm',
                   user=new_user, token=token)

        flash("Para finalizar o cadastro, foi enviado a confirmação para o seu email.", category="success")
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@auth_blueprint.route('/confirm/<token>')
def confirm(token):
    result, user_id = User.verify_token("confirm", token)
    if result:
        user = User.query.filter_by(id=user_id).one()
        if user is not None and not user.confirmed:
            user.set_confirmed(True)
            db.session.add(user)
            db.session.commit()
            flash('Sua conta foi confirmada, Obrigado', category='success')
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    else:
        flash('O link para confirmação é invalido ou está expirado!', category='error')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/<string:username>/confirm', methods=['GET', 'POST'])
def resend_confirmation(username):
    user = User.query.filter_by(username=username).one()
    token = user.create_token("confirm")
    send_email(user.email,
               'Confirmação de Conta',
               'auth/email/confirm',
               user=user, token=token)

    flash("Um novo email de confirmação foi enviado para o seu email.", category="success")
    return redirect(url_for('main.index'))


# alteração de senha quando logado
@auth_blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Sua senha foi atualizada", category="sucess")
            return redirect(url_for('main.index'))
        else:
            flash('Senha inválida', category="error")
    return render_template("auth/change_password.html", form=form)


# solicitação de nova senha
@auth_blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.create_token("reset")
            send_email(user.email,
                       'Redefinição de Senha',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('Um email com instruções para redefinição de senha foi enviado para seu email.',
              category="sucess")
        return redirect(url_for('auth.login'))
    return render_template('auth/request_reset_password.html', form=form)


@auth_blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset_verify_token(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))

    result, user_id = User.verify_token("reset", token)
    if result:
        user = User.query.filter_by(id=user_id).one()
        if user:
            return redirect(url_for('auth.password_reset', token=token))
        return redirect(url_for('main.index'))
    else:
        flash('O link para confirmação é invalido ou está expirado!', category='error')
        return redirect(url_for('main.index'))


@auth_blueprint.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()

    if form.validate_on_submit():
        result, user_id = User.verify_token("reset", token)
        if result:
            user = User.query.filter_by(id=user_id).one()
            if user:
                user.set_password(form.password.data)
                db.session.commit()
                flash('Sua senha foi atualizada.')
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('main.index'))
        else:
            flash('O link para confirmação é invalido ou está expirado!', category='error')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, token=token)
