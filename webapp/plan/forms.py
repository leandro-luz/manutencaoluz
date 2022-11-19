from flask_wtf import FlaskForm as Form
from wtforms import StringField, IntegerField, SelectField, \
    PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from flask import flash
from webapp.plan.models import ViewPlan


class PlanForm(Form):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do plano"})
    view = SelectField('Telas', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        # flash("Empresa não adicionada", category="danger")
        return True


class ViewForm(Form):
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome da tela"})
    icon = StringField('Icone', validators=[DataRequired(), Length(max=50)],
                       render_kw={"placeholder": "Digite o nome do icone"})
    url = StringField('URL', validators=[DataRequired(), Length(max=50)],
                      render_kw={"placeholder": "Digite o endereço da url"})
    submit = SubmitField("Cadastrar")

    def validate(self):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        # flash("Empresa não adicionada", category="danger")
        return True


class ViewPlanForm(Form):
    view = SelectField('Telas', choices=[], coerce=int)
    plan = SelectField('Plano', choices=[], coerce=int)
    submit = SubmitField("Cadastrar")

    def validate(self):
        # if our validators do not pass
        # check_validate = super(CompanyForm, self).validate()
        # if not check_validate:
        #     return False

        if ViewPlan.query.filter_by(plan_id=self.plan.data, view_id=self.view.data).first() is not None:
            flash("Tela já registrada para este plano", category="danger")
            return False

        return True


