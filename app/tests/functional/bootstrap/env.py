import os

http_user = os.environ.get('HTTP_USER', '')
http_pass = os.environ.get('HTTP_PASS', '')
platform = os.environ.get('PLATFORM', '')

APPIUM_STANDALONE = 'http://172.16.0.101:4723/wd/hub'
SELENIUM_GRID_HUB = 'http://172.16.0.101:4444/wd/hub'
IS_PRODUCTION = False

APP_BASE_URL = 'https://{0}:{1}@lotsaluggage.net'.format(http_user, http_pass) \
    if IS_PRODUCTION else 'http://localhost:5000'


