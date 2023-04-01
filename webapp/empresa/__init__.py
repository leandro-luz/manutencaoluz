def create_module(app, **kwargs):
    """    Cria o módulo do controlador - Empresas    """
    from .controllers import empresa_blueprint
    app.register_blueprint(empresa_blueprint)
