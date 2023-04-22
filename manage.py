import os
from webapp import db, migrate, create_app
from webapp.usuario.models import Usuario, Perfil
from webapp.empresa.models import Empresa
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.supplier.models import Supplier
from webapp.contrato.models import Contrato, Telacontrato, Tela

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=Usuario, Role=Perfil,
                Company=Empresa,
                Asset=Equipamento, Group=Grupo, System=Sistema,
                Supplier=Supplier,
                Plan=Contrato, ViewPlan=Telacontrato, View=Tela,
                migrate=migrate)
