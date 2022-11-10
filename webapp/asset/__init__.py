def create_module(app, **kwargs):
    from .controllers import asset_blueprint
    app.register_blueprint(asset_blueprint)













