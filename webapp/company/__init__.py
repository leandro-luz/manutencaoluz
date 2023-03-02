def create_module(app, **kwargs):
    """    Cria o módulo do controlador - Empresas    """
    from .controllers import company_blueprint
    app.register_blueprint(company_blueprint)
