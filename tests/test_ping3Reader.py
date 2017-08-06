import logging
from unittest import TestCase
from ping3.Ping3Proxy import Device, ConfigHolder


class TestPing3Reader(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPing3Reader, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG)

    def test_read(self):
        device_configuration = ConfigHolder("../devices.xml")[0]
        reader = Device(device_configuration.login,
                        device_configuration.password,
                        device_configuration.url,
                        device_configuration.port,
                        3)
        #reader.update()
        self.assertEquals(str(1), reader[Device.PORT_DIGITAL_PREFIX+"1"])
        self.assertEquals(str(1), reader[Device.PORT_DIGITAL_PREFIX+"2"])
        self.assertEquals(str(1), reader[Device.PORT_DIGITAL_PREFIX+"3"])
        self.assertEquals(str(1), reader[Device.PORT_DIGITAL_PREFIX+"4"])

        try:
            self.assertIsNone(reader[Device.PORT_ANALOG_PREFIX+"0"])
            self.assertFalse(True)
        except ( KeyError ):
            pass

        self.assertIsNotNone(reader[Device.PORT_ANALOG_PREFIX+"1"])
        self.assertIsNotNone(reader[Device.PORT_ANALOG_PREFIX+"2"])
        self.assertIsNotNone(reader[Device.PORT_ANALOG_PREFIX+"3"])
        self.assertIsNotNone(reader[Device.PORT_ANALOG_PREFIX+"4"])
        try:
            self.assertIsNone(reader[Device.PORT_ANALOG_PREFIX+"5"])
            self.assertFalse(True)
        except ( KeyError ):
            pass


