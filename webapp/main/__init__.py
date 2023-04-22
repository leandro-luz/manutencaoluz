def criar_modulo(app, **kwargs):
    """Cria o módulo para o controlador Main - Página inicial"""
    from .controllers import main_blueprint
    app.register_blueprint(main_blueprint)
