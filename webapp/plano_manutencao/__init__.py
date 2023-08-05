def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador Plano Manutenção"""
    from .controllers import plano_manutencao_blueprint
    from webapp.plano_manutencao.models import PlanoManutencao

    app.register_blueprint(plano_manutencao_blueprint)
