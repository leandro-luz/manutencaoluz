def create_module(app, **kwargs):
    """Cria o modulo para o contraldor do Sistema - Páginas do sistema"""
    from .controllers import sistema_blueprint
    app.register_blueprint(sistema_blueprint)
