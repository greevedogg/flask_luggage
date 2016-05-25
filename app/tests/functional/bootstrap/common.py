from env import SELENIUM_GRID_HUB, platform, APPIUM_STANDALONE, APP_BASE_URL

SELENIUM_HUB = SELENIUM_GRID_HUB if 'ios' not in platform else APPIUM_STANDALONE

if 'ios' in platform:
    CAPABILITIES = {
      'platformName': 'iOS',
      'platformVersion': '9.2',
      'browserName': 'Safari',
      'deviceName': 'iPad Air 2',
      'safariIgnoreFraudWarning': True,
      # 'nativeWebTap': True,
      'nonSyntheticWebClick': False,
    }
else:
    CAPABILITIES = {
        'platformName': 'MAC',
        'browserName': 'firefox'
    }