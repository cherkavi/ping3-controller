from unittest import TestCase
from Ping3Proxy import Reader
import logging

class TestPing3Reader(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestPing3Reader, cls).setUpClass()
        logging.basicConfig(level=logging.DEBUG)

    def test_read(self):
        reader = Reader("admin", "fenics", "212.90.56.52", 93, 3)
        self.assertEquals(str(1), reader.value(1))