#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Datasource
   @package: test.datasource
      @file: test_sqlite_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright·(c)·2024,·HSPyLib
"""

from datasource.db_configuration import DBConfiguration
from datasource.identity import Identity
from hspylib.core.namespace import Namespace
from hspylib.core.tools.commons import log_init
from hspylib.core.tools.text_tools import quote
from shared.entity_test import EntityTest
from shared.sqlite_repository_test import SQLiteRepositoryTest
from textwrap import dedent

import logging as log
import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):
    # Setup tests
    @classmethod
    def setUpClass(cls) -> None:
        log_init(console_enable=True)
        resource_dir = "{}/resources".format(TEST_DIR)
        config = DBConfiguration(resource_dir, profile="test")
        log.info(config)
        repository = SQLiteRepositoryTest(config)
        repository.execute(
            dedent(
                """
        CREATE TABLE IF NOT EXISTS "ENTITY_TEST"
        (
            id           TEXT       not null,
            comment      TEXT       not null,
            lucky_number INTEGER    not null,
            is_working   TEXT       not null,

            CONSTRAINT ID_pk PRIMARY KEY (id)
        )
        """
            )
        )
        cls.repository = repository

    def setUp(self) -> None:
        self.repository.execute("DELETE FROM ENTITY_TEST")

    # TEST CASES ----------

    # Test updating a single object from sqlite.
    def test_should_update_sqlite_database(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        test_entity.comment = "Updated My-Test Data"
        self.repository.save(test_entity)
        result_set = self.repository.find_all(filters=Namespace(by_id=f"id = {quote(test_entity.id)}"))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, list)
        self.assertEqual(1, len(result_set))
        result_one = result_set[0]
        self.assertEqual(test_entity.id, result_one.id)
        self.assertEqual(test_entity.comment, result_one.comment)
        self.assertEqual(test_entity.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity.is_working, result_one.is_working)

    # Test selecting all objects from sqlite.
    def test_should_select_all_from_sqlite(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.save_all([test_entity_1, test_entity_2])
        result_set = self.repository.find_all()
        self.assertIsNotNone(result_set, "Result set is none")
        expected_list = [test_entity_1, test_entity_2]
        self.assertCountEqual(expected_list, result_set)

    # Test selecting a single object from sqlite.
    def test_should_select_one_from_sqlite(self) -> None:
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

    # Test deleting one object from sqlite.
    def test_should_delete_from_sqlite(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        result_one = self.repository.find_by_id(test_entity.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity.id, result_one.id)
        self.repository.delete(test_entity)
        result_one = self.repository.find_by_id(test_entity.identity)
        self.assertIsNone(result_one, "Result set is not empty")

    # Test selecting from sqlite using filters
    def test_should_select_using_filters_from_sqlite(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data-1", lucky_number=50, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Work Data-2", lucky_number=40, is_working=False)
        test_entity_3 = EntityTest(Identity.auto(), comment="My-Sets Data-3", lucky_number=30, is_working=True)
        test_entity_4 = EntityTest(Identity.auto(), comment="My-Fest Data-4", lucky_number=20, is_working=False)
        expected_list = [test_entity_1, test_entity_2, test_entity_3, test_entity_4]
        self.repository.save_all(expected_list)
        result_set = self.repository.find_all()
        self.assertCountEqual(expected_list, result_set)
        expected_list = [test_entity_1, test_entity_4]
        result_set = self.repository.find_all(filters=Namespace(by_comment="comment like '%est%'"))
        self.assertCountEqual(expected_list, result_set)
        result_set = self.repository.find_all(order_bys=["lucky_number"])
        expected_list = [test_entity_4, test_entity_3, test_entity_2, test_entity_1]
        self.assertEqual(expected_list[0], result_set[0])
        self.assertEqual(expected_list[1], result_set[1])
        self.assertEqual(expected_list[2], result_set[2])
        self.assertEqual(expected_list[3], result_set[3])


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
