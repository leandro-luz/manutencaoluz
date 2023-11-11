def criar_modulo(app, **kwargs):
    """Cria o módulo do controlador - Equipamentos"""
    from .controllers import equipamento_blueprint
    app.register_blueprint(equipamento_blueprint)
