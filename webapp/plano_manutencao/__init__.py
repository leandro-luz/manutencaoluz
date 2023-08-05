def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador Plano Manutenção"""
    from datetime import datetime, timedelta
    from .controllers import plano_manutencao_blueprint
    from webapp.plano_manutencao.models import PlanoManutencao

    app.register_blueprint(plano_manutencao_blueprint)

    # # Programação para geração das ordens serviços automaticamente
    # sched.add_job(id='ordens_servico_automaticas',
    #               func=PlanoManutencao.verificar_geracao_ordens_servicos,
    #               trigger='interval',
    #               start_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) +
    #                          timedelta(days=1), days=1)
