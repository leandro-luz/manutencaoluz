def create_module(app, **kwargs):
    """Cria o módulo do contralador Asset - Equipamentos"""
    from .controllers import asset_blueprint
    app.register_blueprint(asset_blueprint)













