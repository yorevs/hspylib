#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.modules.mock
      @file: test_mock_server.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import os
import sys
import unittest

import requests

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.enums.http_code import HttpCode
from hspylib.core.enums.http_method import HttpMethod
from mock.mock_server import MockServer

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = "{}/resources".format(TEST_DIR)
        os.environ["ACTIVE_PROFILE"] = "test"
        self.configs = AppConfigs(resource_dir=resource_dir)
        self.server = MockServer("localhost", MockServer.RANDOM_PORT)
        self.server.start()

    # Teardown tests
    def tearDown(self):
        self.server.stop()

    # TEST CASES ----------

    # TC1 - Test processing a get stubbed request.
    def test_should_process_a_get_request(self):
        endpoint = "/test-get"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        expected_body = '{"status": "done"}'
        expected_etag_header = {"Etag": "12345678"}
        self.server.when_request(HttpMethod.GET, endpoint).then_return(HttpCode.OK, expected_body, expected_etag_header)
        resp = requests.get(url)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.OK.code, resp.status_code)
        self.assertEqual(expected_body, resp.text)
        self.assertEqual(resp.headers["Etag"], expected_etag_header["Etag"])

    # TC2 - Test processing a post stubbed request.
    def test_should_process_a_post_request(self):
        endpoint = "/test-post"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        expected_body = '{"status": "done"}'
        expected_etag_header = {"Etag": "12345678"}
        self.server.when_request(HttpMethod.POST, endpoint).then_return_with_received_body(
            HttpCode.OK, expected_etag_header
        )
        resp = requests.post(url, data=expected_body)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.OK.code, resp.status_code)
        self.assertEqual(expected_body, resp.text)
        self.assertEqual(resp.headers["Etag"], expected_etag_header["Etag"])

    # TC3 - Test processing a put stubbed request.
    def test_should_process_a_put_request(self):
        endpoint = "/test-put"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        expected_body = '{"id": "10", "status": "done"}'
        expected_etag_header = {"Etag": "12345678"}
        self.server.when_request(HttpMethod.PUT, endpoint).then_return(
            HttpCode.CREATED, expected_body, expected_etag_header
        )
        resp = requests.put(url, data=expected_body)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.CREATED.code, resp.status_code)
        self.assertEqual(expected_body, resp.text)
        self.assertEqual(resp.headers["Etag"], expected_etag_header["Etag"])

    # TC4 - Test processing a patch stubbed request.
    def test_should_process_a_patch_request(self):
        endpoint = "/test-patch"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        expected_body = '{"status": "done"}'
        expected_etag_header = {"Etag": "987654321"}
        self.server.when_request(HttpMethod.PATCH, endpoint).then_return(
            HttpCode.ACCEPTED, expected_body, expected_etag_header
        )
        resp = requests.patch(url, data=expected_body)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.ACCEPTED.code, resp.status_code)
        self.assertEqual(expected_body, resp.text)
        self.assertEqual(resp.headers["Etag"], expected_etag_header["Etag"])

    # TC5 - Test processing a delete stubbed request.
    def test_should_process_a_delete_request(self):
        endpoint = "/test-delete"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        self.server.when_request(HttpMethod.DELETE, endpoint).then_return(HttpCode.OK)
        resp = requests.delete(url)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.OK.code, resp.status_code)
        self.assertEqual("", resp.text)

    # TC6 - Test processing menu_options request.
    #       When there is a method stubbed and path is not found, return 'not found'; otherwise 'method not allowed'.
    def test_should_process_options_request(self):
        endpoint = "/test-menu_options"
        url = "http://localhost:{}{}".format(self.server.port, endpoint)
        resp = requests.options(url)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.NO_CONTENT.code, resp.status_code)
        self.assertEqual(resp.headers["Allow"], "OPTIONS")
        self.server.when_request(HttpMethod.GET, endpoint).then_return_with_received_body(HttpCode.OK)
        resp = requests.options(url)
        self.assertIsNotNone(resp, "Response is empty")
        self.assertEqual(HttpCode.NO_CONTENT.code, resp.status_code)
        self.assertEqual(resp.headers["Allow"], "OPTIONS, GET")
        resp = requests.get("{}/notfound".format(url))
        self.assertTrue(not resp, "Response is not empty")
        self.assertEqual(HttpCode.NOT_FOUND.code, resp.status_code)
        resp = requests.patch(url)
        self.assertTrue(not resp, "Response is not empty")
        self.assertEqual(HttpCode.METHOD_NOT_ALLOWED.code, resp.status_code)


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
