import os
from webapp import db, migrate, create_app
from webapp.usuario.models import Usuario, Perfil
from webapp.empresa.models import Empresa, Subbusiness, Business
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.supplier.models import Supplier
from webapp.plano.models import Plano, Telaplano, Tela

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=Usuario, Role=Perfil,
                Company=Empresa, Subbusiness=Subbusiness, Business=Business,
                Asset=Equipamento, Group=Grupo, System=Sistema,
                Supplier=Supplier,
                Plan=Plano, ViewPlan=Telaplano, View=Tela,
                migrate=migrate)
