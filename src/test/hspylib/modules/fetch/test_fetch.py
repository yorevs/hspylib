import sys
import unittest

from main.hspylib.core.enum.http_code import HttpCode
from main.hspylib.core.enum.http_method import HttpMethod
from main.hspylib.modules.mock.mock_server import MockServer
from src.main.hspylib.modules.fetch.fetch import get, post, put, patch, delete


class TestFetch(unittest.TestCase):

    def setUp(self):
        self.server_mock = MockServer('localhost', MockServer.RANDOM_PORT)
        self.server_mock.start()

    def tearDown(self):
        self.server_mock.stop()

    def test_should_get_from_server(self):
        expected_resp = '{"name":"Mock Server"}'
        self.server_mock \
            .when_request(HttpMethod.GET, '/get') \
            .then_return(HttpCode.OK, expected_resp)
        resp = get('localhost:{}/get'.format(self.server_mock.port))
        assert resp, "Response is empty or None"
        self.assertEqual(expected_resp, resp.decode('utf-8'))

    def test_should_post_to_server(self):
        expected_resp = '{"name":"Mock Server"}'
        self.server_mock \
            .when_request(HttpMethod.POST, '/post') \
            .then_return(HttpCode.CREATED, expected_resp)
        resp = post('localhost:{}/post'.format(self.server_mock.port), expected_resp)
        assert resp, "Response is empty or None"
        self.assertEqual(expected_resp, resp.decode('utf-8'))

    def test_should_put_to_server(self):
        expected_resp = '{"name":"Mock Server"}'
        self.server_mock \
            .when_request(HttpMethod.PUT, '/put') \
            .then_return(HttpCode.OK, expected_resp)
        resp = put('localhost:{}/put'.format(self.server_mock.port), expected_resp)
        assert resp, "Response is empty or None"
        self.assertEqual(expected_resp, resp.decode('utf-8'))

    def test_should_patch_to_server(self):
        expected_resp = '{"name":"Mock Server"}'
        self.server_mock \
            .when_request(HttpMethod.PATCH, '/patch') \
            .then_return(HttpCode.ACCEPTED, expected_resp)
        resp = patch('localhost:{}/patch'.format(self.server_mock.port), expected_resp)
        assert resp, "Response is empty or None"
        self.assertEqual(expected_resp, resp.decode('utf-8'))

    def test_should_delete_from_server(self):
        self.server_mock \
            .when_request(HttpMethod.DELETE, '/delete') \
            .then_return(HttpCode.OK)
        resp = delete('localhost:{}/delete'.format(self.server_mock.port))
        assert not resp, "Response is empty or None"


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFetch)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
