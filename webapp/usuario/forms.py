from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp
from webapp.usuario.models import Usuario, ViewRole
from webapp.empresa.models import Empresa
from flask import flash
from flask_login import current_user


class LoginForm(Form):
    nome = StringField('Usuário', validators=[InputRequired(), Length(max=255)],
                           render_kw={"placeholder": "Digite o seu nome"})
    # email = StringField('Email', validators=[InputRequired(), Email()],
    #                     render_kw={"placeholder": "Digite o seu email"})
    senha = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    # remember = BooleanField("Me lembre")
    submit = SubmitField("Enviar")

    def validate(self, **kwargs):
        check_validate = super(LoginForm, self).validate()

        if check_validate:
            # Verifica se o usuário existe
            usuario = Usuario.query.filter_by(nome=self.nome.data).one_or_none()
            if not usuario:
                flash("Usuário ou senha não válidos!", category="danger")
                return False

            # Verifica se a senha está válida
            if usuario.senha.verificar_senha(self.senha.data):
                # Verifica se a senha é expirável e se não está expirada
                if usuario.senha.senha_expira and not usuario.senha.verificar_data_expiracao():
                    return False
            else:
                flash("Usuário ou senha não válidos!", category="danger")
                return False

            # Verifica se o usuário está com a senha temporária
            if usuario.senha.senha_temporaria:
                valor = usuario.senha.contador_acesso_temporario + 1
                if valor <= 3:
                    usuario.senha.alterar_contador_accesso_temporario()
                    usuario.senha.salvar()
                    flash(f'Usuário está com a senha temporária, permitido mais {3-valor} acesso(s)', category="warning")
                elif valor > 3:
                    flash(f'Usuário está com a senha temporária vencida! Deve trocar a senha', category="danger")
                    return False

            # Verifica se a empresa está ativa
            empresa = Empresa.query.filter_by(id=usuario.empresa_id).one_or_none()
            if not empresa.ativo:
                flash("Empresa não está ativa!", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário ou senha não válidos!", category="danger")
            return False

        return True


class RegistroUsuarioForm(Form):
    nome = StringField('Usuário', [InputRequired(), Length(max=50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Nome deve conter somente letras, '
                                              'números, ponto ou sublinha')],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', [InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    senha = PasswordField('Senha', [InputRequired(), Length(min=8)],
                             render_kw={"placeholder": "Digite a sua senha"})
    empresa = SelectField('Empresa', choices=[], coerce=int)
    active = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a usuário está ativo"})

    confirm = PasswordField('Confirme a Senha', [InputRequired(), EqualTo('senha')],
                            render_kw={"placeholder": "Confirme a sua senha"})
    submit = SubmitField('Registrar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(RegistroUsuarioForm, self).validate()
        if check_validate:

            # Verifica se já existe um usuário com o mesmo nome
            usuario = Usuario.query.filter_by(nome=self.nome.data).first()
            if usuario:
                flash("Usuário já cadastrado com este nome", category="danger")
                return False

            # Verifica se existe um usuário com o mesmo email
            usuario = Usuario.query.filter_by(email=self.email.data).first()
            if usuario:
                flash("Usuário já cadastrado com este email", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário não validada", category="danger")
            return False
        return True


class EditarUsuarioForm(Form):
    nome = StringField('Usuário', [InputRequired(), Length(max=50),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Nome deve conter somente letras, '
                                              'números, ponto ou sublinha')],
                           render_kw={"placeholder": "Digite o seu nome"})
    email = StringField('Email', [InputRequired(), Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    empresa = SelectField('Empresa', choices=[], coerce=int)
    perfil = SelectField('Perfil', choices=[], coerce=int)
    ativo = BooleanField('Ativo',
                          render_kw={"placeholder": "Informe se a usuário está ativo"})

    submit = SubmitField('Registrar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(EditarUsuarioForm, self).validate()
        if check_validate:
            # Verifica se já existe um usuário com o mesmo nome
            usuario = Usuario.query.filter_by(nome=self.nome.data).first()
            if usuario:
                flash("Usuário já cadastrado com este nome", category="danger")
                return False

            # Verifica se existe um usuário com o mesmo email
            usuario = Usuario.query.filter_by(email=self.email.data).first()
            if usuario:
                flash("Usuário já cadastrado com este email", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            flash("Usuário não validada", category="danger")
            return False

        return True


class AlterarSenhaForm(Form):
    senha_antiga = PasswordField('Senha antiga', validators=[InputRequired()],
                                 render_kw={"placeholder": "Digite a senha antiga"})
    senha = PasswordField('Nova senha', validators=[
        InputRequired(), EqualTo('password2', message='As senhas devem ser iguais!')],
                             render_kw={"placeholder": "Digite a nova senha"})
    senha2 = PasswordField('Confirme a nova senha',
                              validators=[InputRequired()],
                              render_kw={"placeholder": "Confirme a nova senha"})
    submit = SubmitField('Atualizar')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(AlterarSenhaForm, self).validate()
        if check_validate:
            if not current_user.senha.verificar_senha(self.senha_antiga.data):
                flash("Senha antiga não está correta", category="danger")
                return False
        else:
            for error in self.errors:
                print(error)
            return False

        return True


class SolicitarNovaSenhaForm(Form):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),
                                             Email()],
                        render_kw={"placeholder": "Digite o seu email"})
    submit = SubmitField('Reset Senha')

    def validate(self, **kwargs):
        # if our validators do not pass
        check_validate = super(SolicitarNovaSenhaForm, self).validate()
        if check_validate:
            return True
        else:
            for error in self.errors:
                print(error)
            return False


class PasswordResetForm(Form):
    senha = PasswordField('Nova Senha', validators=[
        InputRequired(), EqualTo('password2', message='As senhas devem ser iguais')])
    senha2 = PasswordField('Confirme a Senha', validators=[InputRequired()])
    submit = SubmitField('Reset Senha')

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
    senha = PasswordField('Senha', validators=[InputRequired()],
                             render_kw={"placeholder": "Digite a sua senha"})
    submit = SubmitField('Atualizar')

    def validate(self, **kwargs):
        if Usuario.query.filter_by(email=self.email.data.lower()).first() is not None:
            flash("Email já registrado", category="danger")
            return False

        return True


class RoleForm(Form):
    nome = StringField('Perfil', validators=[InputRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do perfil"})
    descricao = StringField('Descrição', validators=[InputRequired(), Length(max=50)],
                              render_kw={"placeholder": "Digite a descrição do perfil"})
    empresa = SelectField('Empresa', choices=[], coerce=int)
    tela = SelectField('Tela', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        return True


class ViewRoleForm(Form):
    tela = SelectField('Telas', choices=[], coerce=int)
    perfil = SelectField('Perfil', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self, **kwargs):
        # if our validators do not pass
        # check_validate = super(EmpresaForm, self).validate()
        # if not check_validate:
        #     return False

        if ViewRole.query.filter_by(role_id=self.perfil.data, tela_id=self.tela.data).first() is not None:
            flash("Tela já registrada para este perfil", category="danger")
            return False

        return True
