def create_module(app, **kwargs):
    from .controllers import sistema_blueprint
    app.register_blueprint(sistema_blueprint)
