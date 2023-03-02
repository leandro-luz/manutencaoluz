import os
from webapp import db, migrate, create_app
from webapp.auth.models import User, Role
from webapp.company.models import Company, Subbusiness, Business
from webapp.asset.models import Asset, Group, System
from webapp.supplier.models import Supplier
from webapp.plan.models import Plan, ViewPlan, View

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                User=User, Role=Role,
                Company=Company, Subbusiness=Subbusiness, Business=Business,
                Asset=Asset, Group=Group, System=System,
                Supplier=Supplier,
                Plan=Plan, ViewPlan=ViewPlan, View=View,
                migrate=migrate)
