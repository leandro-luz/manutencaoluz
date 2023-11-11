def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador - Fornecedor"""
    from .controllers import supplier_blueprint
    app.register_blueprint(supplier_blueprint)
