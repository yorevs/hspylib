#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.test.hspylib.modules.fetch
      @file: test_fetch.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import os
import sys
import unittest

from requests.exceptions import ConnectTimeout, ConnectionError

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from hspylib.modules.fetch.fetch import delete, get, head, patch, post, put, is_reachable
from hspylib.modules.mock.mock_server import MockServer

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestFetch(unittest.TestCase):

    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        self.mock_server = MockServer('localhost', MockServer.RANDOM_PORT)
        self.mock_server.start()

    def tearDown(self):
        self.mock_server.stop()

    def test_should_get_from_server(self):
        expected_code = HttpCode.OK
        expected_resp = '{"name":"Mock Server"}'
        self.mock_server \
            .when_request(HttpMethod.GET, '/get') \
            .then_return(code=expected_code, body=expected_resp)
        resp = get('localhost:{}/get'.format(self.mock_server.port))
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")
        self.assertEqual(expected_resp, resp.body)

    def test_should_head_from_server(self):
        expected_code = HttpCode.OK
        self.mock_server \
            .when_request(HttpMethod.HEAD, '/head') \
            .then_return(code=expected_code)
        resp = head('localhost:{}/head'.format(self.mock_server.port))
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")

    def test_should_post_to_server(self):
        expected_code = HttpCode.CREATED
        expected_resp = '{"name":"Mock Server"}'
        self.mock_server \
            .when_request(HttpMethod.POST, '/post') \
            .then_return_with_received_body(code=expected_code)
        resp = post('localhost:{}/post'.format(self.mock_server.port), expected_resp)
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")
        self.assertEqual(expected_resp, resp.body)

    def test_should_put_to_server(self):
        expected_code = HttpCode.OK
        expected_resp = '{"name":"Mock Server"}'
        self.mock_server \
            .when_request(HttpMethod.PUT, '/put') \
            .then_return_with_received_body(code=expected_code)
        resp = put('localhost:{}/put'.format(self.mock_server.port), expected_resp)
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")
        self.assertEqual(expected_resp, resp.body)

    def test_should_patch_to_server(self):
        expected_code = HttpCode.ACCEPTED
        expected_resp = '{"name":"Mock Server"}'
        self.mock_server \
            .when_request(HttpMethod.PATCH, '/patch') \
            .then_return_with_received_body(code=expected_code)
        resp = patch('localhost:{}/patch'.format(self.mock_server.port), expected_resp)
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")
        self.assertEqual(expected_resp, resp.body)

    def test_should_delete_from_server(self):
        expected_code = HttpCode.OK
        self.mock_server \
            .when_request(HttpMethod.DELETE, '/delete') \
            .then_return(code=expected_code)
        resp = delete('localhost:{}/delete'.format(self.mock_server.port))
        self.assertEqual(expected_code, resp.status_code)
        self.assertIsNotNone(resp, "Response is none")
        self.assertTrue(resp.body == '', "Response is not empty")

    def test_should_except_when_read_timeout_expires(self):
        self.assertRaisesRegex(
            ConnectTimeout, '.*\(connect timeout=1\).*',
            lambda: get('240.0.0.0', timeout=1))

    def test_should_except_when_connect_timeout_expires(self):
        self.assertRaisesRegex(
            ConnectionError, '.*\(connect timeout=1\).*',
            lambda: get('example.com:9999', timeout=1))

    def test_should_be_reachable(self):
        self.assertTrue(is_reachable('example.com'))

    def test_should_not_be_reachable(self):
        self.assertFalse(is_reachable('example.com:9999'))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFetch)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
