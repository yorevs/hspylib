import sys
import unittest

from src.main.hspylib.modules.fetch.fetch import get
from src.main.hspylib.modules.server_mock.server_mock import ServerMock


class TestEventBus(unittest.TestCase):

    def setUp(self):
        self.server_mock = ServerMock()

    def tearDown(self):
        pass

    def test_should_get_from_example_com(self):
        resp = get('http://example.com')
        self.assertIsNotNone(resp)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEventBus)
    unittest\
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout)\
        .run(suite)
