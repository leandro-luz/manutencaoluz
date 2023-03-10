from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
from webapp.auth.models import User, ViewRole
from webapp.company.models import Company
from flask import flash
from flask_login import current_user


class LoginForm(Form):
    username = StringField('Usuário', validators=[InputRequired(), Length(max=255)],
                           render_kw={"placeholder": "Digite o seu nome"})
    # email = StringField('Email', validators=[InputRequired(), Email()],
    #                     render_kw={"placeholder": "Digite o seu email"})
    password = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    # remember = BooleanField("Me lembre")
    submit = SubmitField("Enviar")

    def validate(self, **kwargs):
        check_validate = super(LoginForm, self).validate()

        if check_validate:
            # Verifica se o usuário existe
            user = User.query.filter_by(username=self.username.data).one_or_none()
            if not user:
                flash("Usuário ou senha não válidos!", category="danger")
                return False

            # Verifica se a senha está válida
            if user.password.check_password(self.password.data):
                # Verifica se a senha é expirável e se não está expirada
                if user.password.expirate and not user.password.verify_expiration_date():
                    return False
            else:
                flash("Usuário ou senha não válidos!", category="danger")
                return False

            # Verifica se o usuário está com a senha temporária
            if user.password.temporary:
                valor = user.password.cont_access_temporary + 1
                if valor <= 3:
                    user.password.set_cont_access_temporary()
                    user.password.save()
                    flash(f'Usuário está com a senha temporária, permitido mais {3-valor} acesso(s)', category="warning")
                elif valor > 3:
                    flash(f'Usuário está com a senha temporária vencida! Deve trocar a senha', category="danger")
                    return False

            # Verifica se a empresa está ativa
            company = Company.query.filter_by(id=user.company_id).one_or_none()
            if not company.active:
                flash("Empresa não está ativa!", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário ou senha não válidos!", category="danger")
            return False

        return True


class RegisterForm(Form):
    username = StringField('Usuário', [InputRequired(), Length(max=50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Nome deve conter somente letras, '
                                              'números, ponto ou sublinha')],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', [InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    password = PasswordField('Senha', [InputRequired(), Length(min=8)],
                             render_kw={"placeholder": "Digite a sua senha"})
    company = SelectField('Empresa', choices=[], coerce=int)
    active = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a usuário está ativo"})

    confirm = PasswordField('Confirme a Senha', [InputRequired(), EqualTo('password')],
                            render_kw={"placeholder": "Confirme a sua senha"})
    submit = SubmitField('Registrar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(RegisterForm, self).validate()
        if check_validate:

            # Verifica se já existe um usuário com o mesmo nome
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                flash("Usuário já cadastrado com este nome", category="danger")
                return False

            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                flash("Usuário já cadastrado com este email", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário não validada", category="danger")
            return False
        return True


class EditForm(Form):
    username = StringField('Usuário', [InputRequired(), Length(max=50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Nome deve conter somente letras, '
                                              'números, ponto ou sublinha')],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', [InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    company = SelectField('Empresa', choices=[], coerce=int)
    role = SelectField('Perfil', choices=[], coerce=int)
    active = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a usuário está ativo"})

    submit = SubmitField('Registrar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(EditForm, self).validate()
        if check_validate:
            # Verifica se já existe um usuário com o mesmo nome
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                flash("Usuário já cadastrado com este nome", category="danger")
                return False

            # Verifica se existe um usuário com o mesmo email
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                flash("Usuário já cadastrado com este email", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário não validada", category="danger")
            return False

        return True


class ChangePasswordForm(Form):
    old_password = PasswordField('Senha antiga', validators=[InputRequired()],
                                 render_kw={"placeholder": "Digite a senha antiga"})
    password = PasswordField('Nova senha', validators=[
        InputRequired(), EqualTo('password2', message='As senhas devem ser iguais!')],
                             render_kw={"placeholder": "Digite a nova senha"})
    password2 = PasswordField('Confirme a nova senha',
                              validators=[InputRequired()],
                              render_kw={"placeholder": "Confirme a nova senha"})
    submit = SubmitField('Atualizar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(ChangePasswordForm, self).validate()
        if check_validate:
            if not current_user.password.check_password(self.old_password.data):
                flash("Senha antiga não está correta", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            return False

        return True


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    submit = SubmitField('Reset Password')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(PasswordResetRequestForm, self).validate()
        if check_validate:
            return True
        else:
            for error in self.errors:
                print(error)
            return False


class PasswordResetForm(Form):
    password = PasswordField('Nova Senha', validators=[
        InputRequired(), EqualTo('password2', message='As senhas devem ser iguais')])
    password2 = PasswordField('Confirme a Senha', validators=[InputRequired()])
    submit = SubmitField('Reset Password')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(PasswordResetForm, self).validate()
        if check_validate:
            return True
        else:
            for error in self.errors:
                print(error)
            return False


class ChangeEmailForm(Form):
    email = StringField('Novo Email', validators=[InputRequired(), Length(1, 64),
                                                  Email()],
                        render_kw={"placeholder": "Digite o novo email"})
    password = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    submit = SubmitField('Atualizar')

    def validate(self, **kwargs):
        if User.query.filter_by(email=self.email.data.lower()).first() is not None:
            flash("Email já registrado", category="danger")
            return False

        return True


class RoleForm(Form):
    name = StringField('Perfil', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do perfil"})
    description = StringField('Descrição', validators=[InputRequired(), Length(max=50)],
                              render_kw={"placeholder": "Digite a descrição do perfil"})
    company = SelectField('Empresa', choices=[], coerce=int)
    view = SelectField('Tela', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        return True


class ViewRoleForm(Form):
    view = SelectField('Telas', choices=[], coerce=int)
    role = SelectField('Perfil', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        if ViewRole.query.filter_by(role_id=self.role.data, view_id=self.view.data).first() is not None:
            flash("Tela já registrada para este perfil", category="danger")
            return False

        return True
