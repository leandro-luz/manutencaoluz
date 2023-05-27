def criar_modulo(app, **kwargs):
    """Cria o módulo do contralador Equipamento - Equipamentos"""
    from .controllers import equipamento_blueprint
    app.register_blueprint(equipamento_blueprint)













