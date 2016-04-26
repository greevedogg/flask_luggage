import os
basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_BASE = os.path.join(basedir, 'Luggage.db')
MAX_SEARCH_RESULTS = 10
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'luggageapp'

PRODUCTION = "production"
DEVELOPMENT = "development"
TESTING = "testing"
VAGRANT = "vagrant"
DEFAULT = "default"

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'f57a4ed6-6fc3-4aa3-9bf9-e73328cb4b83'
    USERNAME = 'admin'
    PASSWORD = 'default'
    SQLALCHEMY_POOL_RECYCLE = 50  # Fixes MySQL lost connection error

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DATABASE
    SECRET_KEY = '2b918f79-c95a-49b1-a89d-c6c86d7e6081'

class ProductionConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://greevedogg:' + os.getenv('MYSQL_PASSWORD', '') + '@greevedogg.mysql.pythonanywhere-services.com/greevedogg$luggageapp'
    SECRET_KEY = '2b918f79-c95a-49b1-a89d-c6c86d7e6081'

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = '993c77c6-8575-4d32-88dd-1ecdd58298f9'

class VagrantConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://homestead:secret@127.0.0.1:33060/' + MYSQL_DATABASE
    SECRET_KEY = '2b918f79-c95a-49b1-a89d-c6c86d7e6081'

config = {
    PRODUCTION: "app.config.ProductionConfig",
    DEVELOPMENT: "app.config.DevelopmentConfig",
    TESTING: "app.config.TestingConfig",
    VAGRANT: "app.config.VagrantConfig",
    DEFAULT: "app.config.DevelopmentConfig"
}


def configure_app(app):
    app.config.from_envvar('LUGGAGE_SETTINGS', silent=True)
    # TODO: rename FLAKS_CONFIGURATION to FLASK_CONFIGURATION  on PythonAnywhere
    config_name = os.getenv('FLAKS_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
