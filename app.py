import os
from webapp import create_app

env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())

if __name__ == '__main__':
    app.run(use_reloader=False)
