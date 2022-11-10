def create_module(app, **kwargs):
    from .controllers import supplier_blueprint
    app.register_blueprint(supplier_blueprint)

