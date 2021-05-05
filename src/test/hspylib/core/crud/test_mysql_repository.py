#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.test.hspylib.core.crud
      @file: mysql_repository_test.py
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

from pymysql.err import InternalError, OperationalError
from requests.structures import CaseInsensitiveDict

from hspylib.core.config.app_config import AppConfigs
from hspylib.core.tools.commons import syserr
from test.hspylib.shared.decorators import integration_test
from test.hspylib.shared.entity_test import EntityTest
from test.hspylib.shared.mysql_repository_test import MysqlRepositoryTest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


@integration_test
class TestMySqlRepository(unittest.TestCase):
    
    # Setup tests
    def setUp(self):
        resource_dir = '{}/resources'.format(TEST_DIR)
        os.environ['ACTIVE_PROFILE'] = "test"
        self.configs = AppConfigs(
            source_root=TEST_DIR, resource_dir=resource_dir, log_dir=resource_dir
        )
        log.info(self.configs)
        self.repository = MysqlRepositoryTest()
        self.table = self.repository.table_name()
        assert self.repository, "Unable to instantiate TestRepository"
        try:
            self.repository.connect()
            self.assertTrue(self.repository.is_connected())
            self.repository.execute(
                f"""CREATE TABLE {self.table} (
                    UUID varchar(36) NOT NULL, 
                    COMMENT varchar(128), 
                    LUCKY_NUMBER int, 
                    IS_WORKING varchar(5), 
                    PRIMARY KEY (UUID))""", True)
        except (InternalError, OperationalError) as err:
            if f"Table '{self.table}' already exists" in str(err):
                self.repository.execute(f"TRUNCATE TABLE {self.table}", True)
    
    # Teardown tests
    def tearDown(self):
        try:
            self.repository.execute(f"DROP TABLE {self.table}", True)
            self.repository.disconnect()
            self.assertFalse(self.repository.is_connected())
        except (InternalError, OperationalError) as err:
            syserr(str(err))
    
    # TEST CASES ----------
    
    # TC1 - Test inserting a single row into the database.
    def test_should_insert_into_database(self):
        test_entity = EntityTest(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(sql_filters=CaseInsensitiveDict({
            "UUID": '{}'.format(test_entity.uuid)
        }))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
    
    # TC2 - Test updating a single row from the database.
    def test_should_update_database(self):
        test_entity = EntityTest(comment='My-Test Data')
        self.repository.insert(test_entity)
        test_entity.comment = 'Updated My-Test Data'
        self.repository.update(test_entity)
        result_set = self.repository.find_all(sql_filters=CaseInsensitiveDict({
            "UUID": '{}'.format(test_entity.uuid)
        }))
        assert result_set, "Result set is empty"
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.comment, result_set[0].comment)
    
    # TC3 - Test selecting all rows from the database.
    def test_should_select_all_from_database(self):
        test_entity_1 = EntityTest(comment='My-Test Data')
        test_entity_2 = EntityTest(comment='My-Test Data 2')
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_all()
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, list)
        self.assertEqual(2, len(result_set))
        self.assertTrue(all(elem in result_set for elem in [test_entity_1, test_entity_2]))
    
    # TC4 - Test selecting a single rows from the database.
    def test_should_select_one_from_database(self):
        test_entity_1 = EntityTest(comment='My-Test Data')
        test_entity_2 = EntityTest(comment='My-Test Data 2')
        self.repository.insert(test_entity_1)
        self.repository.insert(test_entity_2)
        result_set = self.repository.find_by_id(entity_id=str(test_entity_1.uuid))
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity_1.uuid, result_set.uuid)
    
    # TC5 - Test selecting all rows and bring only specified columns.
    def test_should_select_columns_from_database(self):
        test_entity = EntityTest(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_all(column_set=["UUID"])
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, list)
        self.assertEqual(1, len(result_set))
        self.assertEqual(test_entity.uuid, result_set[0].uuid)
        self.assertIsNone(result_set[0].comment)
    
    # TC6 - Test deleting one row from the database.
    def test_should_delete_from_database(self):
        test_entity = EntityTest(comment='My-Test Data')
        self.repository.insert(test_entity)
        result_set = self.repository.find_by_id(entity_id=str(test_entity.uuid))
        assert result_set, "Result set is empty"
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity.uuid, result_set.uuid)
        self.repository.delete(test_entity)
        assert not self.repository.find_by_id(entity_id=str(test_entity.uuid)), \
            "Result set is not empty"


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMySqlRepository)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
