import os
from webapp import db, migrate, create_app
from webapp.auth.models import User


env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, migrate=migrate)
