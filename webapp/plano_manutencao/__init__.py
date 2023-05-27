def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador Plano Manutenção"""
    from .controllers import plano_manutencao_blueprint
    app.register_blueprint(plano_manutencao_blueprint)

