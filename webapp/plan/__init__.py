def create_module(app, **kwargs):
    from .controllers import plan_blueprint
    app.register_blueprint(plan_blueprint)

