def create_module(app, **kwargs):
    """Cria o módulo do contralador - Planos de assinatura"""
    from .controllers import plano_blueprint
    app.register_blueprint(plano_blueprint)
