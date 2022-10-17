from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
mail = Mail()


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    debug_toolbar.init_app(app)

    from .auth import create_module as auth_create_module
    from .main import create_module as main_create_module
    from .sistema import create_module as sistema_create_module

    auth_create_module(app)
    main_create_module(app)
    sistema_create_module(app)

    # app.register_error_handler(404, page_not_found)
    return app
