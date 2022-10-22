from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from .models import User


class LoginForm(Form):
    username = StringField('Usuário', validators=[DataRequired(), Length(max=255)],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    password = PasswordField('Senha', validators=[DataRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    remember = BooleanField("Me lembre")
    submit = SubmitField("Enviar")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # Does our user exist
        user = User.query.filter_by(username=self.username.data).first()

        if not user:
            self.username.errors.append('Usuário ou senha não válidos')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Usuário ou senha não válidos')
            return False

        return True


class RegisterForm(Form):
    username = StringField('Usuário', [DataRequired(), Length(max=50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Nome deve conter somente letras, '
                                              'números, ponto ou sublinha')],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', [DataRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    password = PasswordField('Senha', [DataRequired(), Length(min=8)],
                             render_kw={"placeholder": "Digite a sua senha"})
    confirm = PasswordField('Confirme a Senha', [DataRequired(), EqualTo('password')],
                            render_kw={"placeholder": "Confirme a sua senha"})
    submit = SubmitField('Registrar')

    def validate(self):
        # if our validators do not pass
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        # Is the username already being used
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Usuário já cadastrado com este nome")
            return False

        # Is the email already being used
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.username.errors.append("Usuário já cadastrado com este email")
            return False

        return True


class ChangePasswordForm(Form):
    old_password = PasswordField('Senha antiga', validators=[DataRequired()],
                                 render_kw={"placeholder": "Digite a senha antiga"})
    password = PasswordField('Nova senha', validators=[
        DataRequired(), EqualTo('password2', message='As senhas devem ser iguais!')],
                             render_kw={"placeholder": "Digite a nova senha"})
    password2 = PasswordField('Confirme a nova senha',
                              validators=[DataRequired()],
                              render_kw={"placeholder": "Confirme a nova senha"})
    submit = SubmitField('Atualizar')

    def validate(self):
        # if our validators do not pass
        check_validate = super(ChangePasswordForm, self).validate()
        if not check_validate:
            return False

        return True


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
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
        DataRequired(), EqualTo('password2', message='As senhas devem ser iguais')])
    password2 = PasswordField('Confirme a Senha', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate(self):
        # if our validators do not pass
        check_validate = super(PasswordResetForm, self).validate()
        if not check_validate:
            return False
        return True


class ChangeEmailForm(Form):
    email = StringField('Novo Email', validators=[DataRequired(), Length(1, 64),
                                                  Email()],
                        render_kw={"placeholder": "Digite o novo email"})
    password = PasswordField('Senha', validators=[DataRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    submit = SubmitField('Atualizar')

    def validate(self):
        if User.query.filter_by(email=self.email.data.lower()).first() is not None:
            return False

        return True
