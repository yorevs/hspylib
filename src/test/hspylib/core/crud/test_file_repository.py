#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud
      @file: test_file_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log
import os
import sys
import unittest

from test.hspylib.core.crud.resources.TestEntity import TestEntity
from test.hspylib.core.crud.resources.TestFileDbRepository import TestFileDbRepository

from hspylib.core.config.app_config import AppConfigs

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):

    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        self.db_file = "{}/test-file-db.txt".format(resource_dir)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        log.info(self.configs)
        self.repository = TestFileDbRepository(self.db_file)

    # Teardown tests
    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    # TEST CASES ----------

    # TC1 - Test inserting a single object into firebase.
    def test_should_insert_into_file_db(self):
        test_entity = TestEntity(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(filters="uuid={}".format(test_entity.uuid))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertEqual(test_entity.comment, result_set[0].comment)
        self.assertEqual(test_entity.lucky_number, result_set[0].lucky_number)
        self.assertEqual(test_entity.is_working, result_set[0].is_working)

    # TC2 - Test updating a single object from firebase.
    def test_should_update_file_db(self):
        test_entity = TestEntity(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        test_entity.comment = 'Updated My-Test Data'
        self.repository.update(test_entity)
        result_set = self.repository.find_all(filters="uuid={}".format(test_entity.uuid))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertEqual(test_entity.comment, result_set[0].comment)
        self.assertEqual(test_entity.lucky_number, result_set[0].lucky_number)
        self.assertEqual(test_entity.is_working, result_set[0].is_working)

    # TC3 - Test selecting all objects from firebase.
    def test_should_select_all_from_file_db(self):
        test_entity_1 = TestEntity(comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = TestEntity(comment='My-Test Data 2', lucky_number=55)
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_all()
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, list)
        self.assertTrue(all(elem in result_set for elem in [test_entity_1, test_entity_2]))

    # TC4 - Test selecting a single object from firebase.
    def test_should_select_one_from_file_db(self):
        test_entity_1 = TestEntity(comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = TestEntity(comment='My-Test Data 2', lucky_number=55)
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_by_id(entity_id=test_entity_1.uuid)
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, TestEntity)
        self.assertEqual(test_entity_1.uuid, result_set.uuid)
        self.assertEqual(test_entity_1.comment, result_set.comment)
        self.assertEqual(test_entity_1.lucky_number, result_set.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_set.is_working)

    # TC5 - Test deleting one object from firebase.
    def test_should_delete_from_file_db(self):
        test_entity = TestEntity(comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.insert(test_entity)
        result_set = self.repository.find_by_id(entity_id=test_entity.uuid)
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, TestEntity)
        self.assertEqual(test_entity.uuid, result_set.uuid)
        self.repository.delete(test_entity)
        result_set = self.repository.find_by_id(entity_id=test_entity.uuid)
        assert not result_set, "Result set is not empty"


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
