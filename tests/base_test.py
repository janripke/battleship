import os
import json
import unittest


class BaseTestCase(unittest.TestCase):
    ENDPOINT = None
    REQUESTS_PROXIES = None

    @classmethod
    def setUpClass(cls):
        environment = os.environ.get('ENVIRONMENT', 'local')

        with open('settings.json') as fp:
            settings = json.load(fp)
            settings = settings[environment]

            cls.ENDPOINT = settings['endpoint']
            cls.REQUESTS_PROXIES = settings.get('requests_proxies')
