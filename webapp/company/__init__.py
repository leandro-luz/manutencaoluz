def create_module(app, **kwargs):
    from .controllers import company_blueprint
    app.register_blueprint(company_blueprint)
