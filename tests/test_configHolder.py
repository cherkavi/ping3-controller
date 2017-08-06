from unittest import TestCase

from ping3.Ping3Proxy import ConfigHolder


class TestConfigHolder(TestCase):
    def test_config(self):
        configHolder = ConfigHolder("../devices.xml")

        self.assertTrue(2, len(configHolder))
        self.assertIsNotNone(configHolder[0].url)
        self.assertIsNotNone(configHolder[0].port)
        self.assertIsNotNone(configHolder[0].login)
        self.assertIsNotNone(configHolder[0].password)