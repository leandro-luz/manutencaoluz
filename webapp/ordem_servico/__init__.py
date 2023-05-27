def criar_modulo(app, **kwargs):
    """Cria o módulo do contralador Ordem Serviço"""
    from .controllers import ordem_servico_blueprint
    app.register_blueprint(ordem_servico_blueprint)

