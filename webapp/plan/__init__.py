def create_module(app, **kwargs):
    """Cria o módulo do contralador - Planos de assinatura"""
    from .controllers import plan_blueprint
    app.register_blueprint(plan_blueprint)
