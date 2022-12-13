#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.datasource
      @file: test_firebase_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from datasource.firebase.firebase_configuration import FirebaseConfiguration
from datasource.identity import Identity
from hspylib.core.decorator.decorators import integration_test
from hspylib.core.tools.commons import log_init
from hspylib.modules.fetch.fetch import delete
from shared.entity_test import EntityTest
from shared.firebase_repository_test import FirebaseRepositoryTest

import logging as log
import os
import sys
import unittest


@integration_test
class TestClass(unittest.TestCase):

    # Setup tests
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["DATASOURCE_PORT"] = "443"
        log_init(file_enable=False, console_enable=True)
        config = FirebaseConfiguration.of_file(os.environ.get("HHS_FIREBASE_CONFIG_FILE"))
        log.info(config)
        cls.repository = FirebaseRepositoryTest(config)

    # Teardown tests
    @classmethod
    def tearDownClass(cls) -> None:
        delete(f"{cls.repository.config.base_url}/hspylib-test/integration-test.json")

    def setUp(self) -> None:
        delete(f"{self.repository.config.base_url}/hspylib-test/integration-test.json")

    # TEST CASES ----------

    # Test updating a single object from firebase.
    def test_should_update_firebase_database(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        test_entity.comment = "Updated My-Test Data"
        self.repository.save(test_entity)
        result_one = self.repository.find_by_id(test_entity.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity.id, result_one.id)
        self.assertEqual(test_entity.comment, result_one.comment)
        self.assertEqual(test_entity.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity.is_working, result_one.is_working)

    # Test selecting all objects from firebase.
    def test_should_select_all_from_firebase(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.save_all([test_entity_1, test_entity_2])
        result_set = self.repository.find_all()
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, list)
        self.assertTrue(all(elem in result_set for elem in [test_entity_1, test_entity_2]))

    # Test selecting a single object from firebase.
    def test_should_select_one_from_firebase(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.save_all([test_entity_1, test_entity_2])
        result_one = self.repository.find_by_id(test_entity_1.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity_1.id, result_one.id)
        self.assertEqual(test_entity_1.comment, result_one.comment)
        self.assertEqual(test_entity_1.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_one.is_working)

    # Test deleting one object from firebase.
    def test_should_delete_from_firebase(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        result_one = self.repository.find_by_id(test_entity.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity.id, result_one.id)
        self.repository.delete(test_entity)
        result_one = self.repository.find_by_id(test_entity.identity)
        self.assertIsNone(result_one, "Result set is not empty")

    # Test selecting from firebase using filters
    def test_should_select_using_filters_from_firebase(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data-1", lucky_number=10, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Work Data-2", lucky_number=20, is_working=False)
        test_entity_3 = EntityTest(Identity.auto(), comment="My-Sets Data-3", lucky_number=30, is_working=True)
        test_entity_4 = EntityTest(Identity.auto(), comment="My-Fest Data-4", lucky_number=40, is_working=False)
        test_entity_5 = EntityTest(Identity.auto(), comment="My-Best Data-5", lucky_number=50, is_working=True)
        expected_list = [test_entity_5, test_entity_4, test_entity_3, test_entity_2, test_entity_1]
        self.repository.save_all(expected_list)
        expected_list = [test_entity_4, test_entity_3, test_entity_2]
        result_set = self.repository.find_all(order_by=["lucky_number"], start_at=20, limit_to_first=3)
        self.assertCountEqual(expected_list, result_set)
        expected_list = [test_entity_5, test_entity_4, test_entity_3]
        result_set = self.repository.find_all(order_by=["lucky_number"], start_at=20, limit_to_last=3)
        self.assertCountEqual(expected_list, result_set)
        expected_list = [test_entity_1, test_entity_3, test_entity_5]
        result_set = self.repository.find_all(order_by=["is_working"], equal_to=True)
        self.assertCountEqual(expected_list, result_set)
        expected_list = [test_entity_3, test_entity_4]
        result_set = self.repository.find_all(order_by=["lucky_number"], start_at=30, end_at=40)
        self.assertCountEqual(expected_list, result_set)


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
