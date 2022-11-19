from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
# debug_toolbar = DebugToolbarExtension()
mail = Mail()


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # debug_toolbar.init_app(app)

    from webapp.auth import create_module as auth_create_module
    from webapp.main import create_module as main_create_module
    from webapp.sistema import create_module as sistema_create_module
    from webapp.company import create_module as company_create_module
    from webapp.asset import create_module as asset_create_module
    from webapp.supplier import create_module as supplier_create_module
    from webapp.plan import create_module as plan_create_module

    auth_create_module(app)
    main_create_module(app)
    sistema_create_module(app)
    company_create_module(app)
    asset_create_module(app)
    supplier_create_module(app)
    plan_create_module(app)

    # app.register_error_handler(404, page_not_found)
    return app
