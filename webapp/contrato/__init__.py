def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador - Planos de assinatura"""
    from .controllers import contrato_blueprint
    app.register_blueprint(contrato_blueprint)
