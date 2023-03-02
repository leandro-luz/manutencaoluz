from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
from webapp.auth.models import User, ViewRole
from flask import flash


class LoginForm(Form):
    username = StringField('Usuário', validators=[InputRequired(), Length(max=255)],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', validators=[InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    password = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    remember = BooleanField("Me lembre")
    submit = SubmitField("Enviar")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # Does our user exist
        user = User.query.filter_by(username=self.username.data).first()

        if not user:
            flash("Usuário ou senha não válidos", category="danger")
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            flash("Usuário ou senha não válidos", category="danger")
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

    def validate(self):
        # if our validators do not pass
        # check_validate = super(RegisterForm, self).validate()
        # if not check_validate:
        #     return False

        # Is the username already being used
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            flash("Usuário já cadastrado com este nome", category="danger")
            return False

        # Is the email already being used
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            flash("Usuário já cadastrado com este email", category="danger")
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

    def validate(self):
        # if our validators do not pass
        # check_validate = super(RegisterForm, self).validate()
        # if not check_validate:
        #     return False

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

    def validate(self):
        # if our validators do not pass
        check_validate = super(ChangePasswordForm, self).validate()
        if not check_validate:
            return False

        return True


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    submit = SubmitField('Reset Password')

    def validate(self):
        # if our validators do not pass
        check_validate = super(PasswordResetRequestForm, self).validate()
        if not check_validate:
            return False

        return True


class PasswordResetForm(Form):
    password = PasswordField('Nova Senha', validators=[
        InputRequired(), EqualTo('password2', message='As senhas devem ser iguais')])
    password2 = PasswordField('Confirme a Senha', validators=[InputRequired()])
    submit = SubmitField('Reset Password')

    def validate(self):
        # if our validators do not pass
        check_validate = super(PasswordResetForm, self).validate()
        if not check_validate:
            return False

        return True


class ChangeEmailForm(Form):
    email = StringField('Novo Email', validators=[InputRequired(), Length(1, 64),
                                                  Email()],
                        render_kw={"placeholder": "Digite o novo email"})
    password = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    submit = SubmitField('Atualizar')

    def validate(self):
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

    def validate(self):
        return True


class ViewRoleForm(Form):
    view = SelectField('Telas', choices=[], coerce=int)
    role = SelectField('Perfil', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        if ViewRole.query.filter_by(role_id=self.role.data, view_id=self.view.data).first() is not None:
            flash("Tela já registrada para este perfil", category="danger")
            return False

        return True
