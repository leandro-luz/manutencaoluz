import os
from webapp import db, migrate, create_app
from webapp.auth.models import User, Role
from webapp.company.models import Company, Subbusiness, Business

env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role,
                Company=Company, Subbusiness=Subbusiness, Business=Business,
                migrate=migrate)
