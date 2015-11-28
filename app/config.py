class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLACHEMY_DATABASE_URI = 'sqlite:///C:/Temp/Luggage.db'

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
    
