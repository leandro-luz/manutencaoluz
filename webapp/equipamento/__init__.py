def create_module(app, **kwargs):
    """Cria o módulo do contralador Equipamento - Equipamentos"""
    from .controllers import empresa_blueprint
    app.register_blueprint(empresa_blueprint)













