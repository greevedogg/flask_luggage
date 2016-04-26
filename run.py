import os
from app import flask_app
import app.config as config


if __name__ == '__main__':
    env = os.getenv('FLAKS_CONFIGURATION', 'default')
    options = {'host': '0.0.0.0'}

    if env is not config.PRODUCTION:
        options['debug'] = True

    flask_app.run(**options)
