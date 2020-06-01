import sys
import unittest
from random import randint

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.mock.mock_server import MockServer
from src.main.hspylib.modules.fetch.fetch import get


class TestFetch(unittest.TestCase):

    def setUp(self):
        self.server_mock = MockServer('localhost', randint(1500, 65000))
        self.server_mock.start()

    def tearDown(self):
        self.server_mock.stop()

    def test_should_get_from_example_com(self):
        expected_resp = '{"name":"yore vs"}'
        self.server_mock \
            .when_request(HttpMethod.GET, '/users') \
            .then_return(HttpCode.OK, expected_resp)
        resp = get('localhost:{}/users'.format(self.server_mock.port))
        self.assertIsNotNone(resp)
        self.assertEqual(expected_resp, resp.decode('utf-8'))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFetch)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
