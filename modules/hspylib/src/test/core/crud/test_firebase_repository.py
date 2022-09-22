#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.crud
      @file: firebase_repository_test.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import logging as log
import os
import sys
import unittest

from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.modules.fetch.fetch import delete
from shared.decorators import integration_test
from shared.entity_test import EntityTest
from shared.firebase_repository_test import FirebaseRepositoryTest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


@integration_test
class TestClass(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(resource_dir=resource_dir)
        log.info(self.configs)
        self.repository = FirebaseRepositoryTest()

    # Teardown tests
    def tearDown(self):
        delete('{}.json'.format(self.repository.config.base_url()))

    # TEST CASES ----------

    # TC1 - Test inserting a single object into firebase.
    def test_should_insert_into_firebase(self):
        test_entity = EntityTest(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(filters=CaseInsensitiveDict({
            "uuid": '{}'.format(test_entity.uuid)
        }))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertEqual(test_entity.comment, result_set[0].comment)
        self.assertEqual(test_entity.lucky_number, result_set[0].lucky_number)
        self.assertEqual(test_entity.is_working, result_set[0].is_working)

    # TC2 - Test updating a single object from firebase.
    def test_should_update_firebase(self):
        test_entity = EntityTest(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        test_entity.comment = 'Updated My-Test Data'
        self.repository.update(test_entity)
        result_set = self.repository.find_all(filters=CaseInsensitiveDict({
            "uuid": '{}'.format(test_entity.uuid)
        }))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertEqual(test_entity.comment, result_set[0].comment)
        self.assertEqual(test_entity.lucky_number, result_set[0].lucky_number)
        self.assertEqual(test_entity.is_working, result_set[0].is_working)

    # TC3 - Test selecting all objects from firebase.
    def test_should_select_all_from_firebase(self):
        test_entity_1 = EntityTest(comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(comment='My-Test Data 2', lucky_number=55)
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_all()
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, list)
        self.assertTrue(all(elem in result_set for elem in [test_entity_1, test_entity_2]))

    # TC4 - Test selecting a single object from firebase.
    def test_should_select_one_from_firebase(self):
        test_entity_1 = EntityTest(comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(comment='My-Test Data 2', lucky_number=55)
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_by_id(entity_id=str(test_entity_1.uuid))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity_1.uuid, result_set.uuid)
        self.assertEqual(test_entity_1.comment, result_set.comment)
        self.assertEqual(test_entity_1.lucky_number, result_set.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_set.is_working)

    # TC5 - Test deleting one object from firebase.
    def test_should_delete_from_firebase(self):
        test_entity = EntityTest(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        result_set = self.repository.find_by_id(entity_id=str(test_entity.uuid))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity.uuid, result_set.uuid)
        self.repository.delete(test_entity)
        result_set = self.repository.find_by_id(entity_id=str(test_entity.uuid))
        self.assertIsNone(result_set, "Result set is not empty")


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
