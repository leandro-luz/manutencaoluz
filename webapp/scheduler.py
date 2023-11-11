import os
import sys
from webapp.utils.tools import data_atual_utc
from webapp import create_app
from webapp.plano_manutencao.models import PlanoManutencao, TipoData
from webapp.ordem_servico.models import OrdemServico

path = "/home/manutencaoluz"
if path not in sys.path:
    sys.path.insert(0, path)

env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())

with app.app_context():
    # Gerando uma lista de planos ativos e que estão pendentes de geração de OS
    planos = PlanoManutencao.query.filter(PlanoManutencao.ativo,
                                          PlanoManutencao.tipodata_id == TipoData.id,
                                          TipoData.nome == "DATA_FIXA"
                                          ).all()

    # se existir uma lista de planos
    if planos:
        # percorrer por toda a lista dos planos
        for plano in planos:
            # Verifica se a data prevista está expirada
            if data_atual_utc() > plano.data_inicio:
                # Alterar a data prevista do plano
                plano.alterar_data_prevista(False)
                # gerar uma OS com status pendente para o plano
                ordem = OrdemServico()
                ordem.alterar_atributos_by_plano(plano)
                # Salvar a ordem de serviço
                ordem.salvar()
                # Salvar o plano com data atualizada
                plano.salvar()
