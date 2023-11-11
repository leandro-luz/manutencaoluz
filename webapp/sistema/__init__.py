def criar_modulo(app, **kwargs):
    """Cria o modulo para o controlador do Sistema - Páginas do sistema"""
    from .controllers import sistema_blueprint
    app.register_blueprint(sistema_blueprint)
