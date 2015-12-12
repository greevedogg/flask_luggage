import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'f57a4ed6-6fc3-4aa3-9bf9-e73328cb4b83'
    USERNAME='admin'
    PASSWORD='default'
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Luggage.db')
    SECRET_KEY = '2b918f79-c95a-49b1-a89d-c6c86d7e6081'

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '993c77c6-8575-4d32-88dd-1ecdd58298f9'

config = {
    "development": "app.config.DevelopmentConfig",
    "testing": "app.config.TestingConfig",
    "default": "app.config.DevelopmentConfig"
}

def configure_app(app):
	app.config.from_envvar('LUGGAGE_SETTINGS', silent=True)
	config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
	app.config.from_object(config[config_name])
    
    
