from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from .models import User


class LoginForm(Form):
    username = StringField('Usuário', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField("Me lembre")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # Does our user exist
        user = User.query.filter_by(username=self.username.data).first()

        if not user:
            self.username.errors.append('Usuário não cadastrado')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.password.errors.append('Senha não válida')
            return False

        return True


class RegisterForm(Form):
    username = StringField('Usuário', [DataRequired(), Length(max=50),
                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                               'Nome deve conter somente letras, '
                                               'números, ponto ou sublinha')])
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Senha', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirme a Senha', [DataRequired(), EqualTo('password')])

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

        return True
