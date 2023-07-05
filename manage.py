import os
from webapp import db, migrate, create_app
from webapp.usuario.models import Usuario, Perfil
from webapp.empresa.models import Empresa
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.supplier.models import Supplier
from webapp.contrato.models import Contrato, Telacontrato, Tela
from webapp.plano_manutencao.models import TipoData, Unidade, Periodicidade, PlanoManutencao
from webapp.ordem_servico.models import SituacaoOrdem, FluxoOrdem, OrdemServico, TramitacaoOrdem

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=Usuario, Perfil=Perfil,
                Empresa=Empresa, Equipamento=Equipamento, Grupo=Grupo,
                Sistema=Sistema, Supplier=Supplier, Contrato=Contrato,
                Telacontrato=Telacontrato, Tela=Tela, TipoData=TipoData,
                Unidade=Unidade, Periodicidade=Periodicidade, PlanoManutencao=PlanoManutencao,
                SituacaoOrdem=SituacaoOrdem, FluxoOrdem=FluxoOrdem, OrdemServico=OrdemServico,
                TramitacaoOrdem=TramitacaoOrdem, migrate=migrate)
