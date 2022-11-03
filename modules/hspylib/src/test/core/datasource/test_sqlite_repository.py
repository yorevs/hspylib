#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.datasource
      @file: test_file_repository.py
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
from textwrap import dedent

from hspylib.core.datasource.identity import Identity
from hspylib.core.datasource.sqlite.sqlite_configuration import SQLiteConfiguration
from hspylib.core.tools.commons import log_init
from hspylib.core.tools.namespace import Namespace
from hspylib.core.tools.text_tools import quote
from shared.entity_test import EntityTest
from shared.sqlite_db_repository_test import SQLiteRepositoryTest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):

    # Setup tests
    @classmethod
    def setUpClass(cls) -> None:
        log_init(file_enable=False, console_enable=True)
        resource_dir = '{}/resources'.format(TEST_DIR)
        config = SQLiteConfiguration(resource_dir, profile="test")
        log.info(config)
        repository = SQLiteRepositoryTest(config)
        repository.execute(dedent("""
        CREATE TABLE IF NOT EXISTS "ENTITY_TEST"
        (
            id           TEXT       not null,
            comment      TEXT       not null,
            lucky_number INTEGER    not null,
            is_working   TEXT       not null,

            CONSTRAINT ID_pk PRIMARY KEY (id)
        )
        """))
        cls.repository = repository

    def setUp(self) -> None:
        self.repository.execute('DELETE FROM ENTITY_TEST')

    # TEST CASES ----------

    # Test updating a single object from firebase.
    def test_should_update_sqlite(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.save(test_entity, exclude_update=['id'])
        test_entity.comment = 'Updated My-Test Data'
        self.repository.save(test_entity, exclude_update=['id'])
        result_set = self.repository.find_all(filters=Namespace(by_id=f"id = {quote(test_entity.id)}"))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, list)
        self.assertEqual(1, len(result_set))
        result_one = result_set[0]
        self.assertEqual(test_entity.id, result_one.id)
        self.assertEqual(test_entity.comment, result_one.comment)
        self.assertEqual(test_entity.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity.is_working, result_one.is_working)

    # Test selecting all objects from firebase.
    def test_should_select_all_from_sqlite(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment='My-Test Data 2', lucky_number=55, is_working=False)
        self.repository.save(test_entity_1)
        self.repository.save(test_entity_2)
        result_set = self.repository.find_all()
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, list)
        self.assertTrue(all(elem in result_set for elem in [test_entity_1, test_entity_2]))

    # Test selecting a single object from firebase.
    def test_should_select_one_from_sqlite(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment='My-Test Data 2', lucky_number=55, is_working=False)
        self.repository.save(test_entity_1)
        self.repository.save(test_entity_2)
        result_one = self.repository.find_by_id(test_entity_1.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity_1.id, result_one.id)
        self.assertEqual(test_entity_1.comment, result_one.comment)
        self.assertEqual(test_entity_1.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_one.is_working)

    # Test deleting one object from firebase.
    def test_should_delete_from_sqlite(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        result_set = self.repository.find_by_id(test_entity.identity)
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity.id, result_set.id)
        self.repository.delete(test_entity)
        result_set = self.repository.find_by_id(test_entity.identity)
        self.assertIsNone(result_set, "Result set is not empty")


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
