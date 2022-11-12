#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.datasource
      @file: test_cassandra_repository.py
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

from hspylib.core.datasource.cassandra.cassandra_configuration import CassandraConfiguration
from hspylib.core.datasource.identity import Identity
from hspylib.core.tools.commons import log_init
from hspylib.core.tools.namespace import Namespace
from hspylib.core.tools.text_tools import quote
from shared.cassandra_repository_test import CassandraRepositoryTest
from shared.entity_test import EntityTest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestClass(unittest.TestCase):

    # Setup tests
    @classmethod
    def setUpClass(cls) -> None:
        os.environ['DATASOURCE_PORT'] = '9042'
        os.environ['DATASOURCE_USERNAME'] = 'astra'
        os.environ['DATASOURCE_PASSWORD'] = 'astra'
        log_init(file_enable=False, console_enable=True)
        resource_dir = '{}/resources'.format(TEST_DIR)
        config = CassandraConfiguration(resource_dir, profile="test")
        log.info(config)
        repository = CassandraRepositoryTest(config)
        repository.execute(dedent(f"""
        CREATE KEYSPACE IF NOT EXISTS {repository.database}
            WITH REPLICATION = """ + """{'class': 'SimpleStrategy', 'replication_factor': 1}
        """))
        repository.execute(dedent(f"""
        CREATE CUSTOM INDEX IF NOT EXISTS comment_idx ON
            {repository.database}.ENTITY_TEST (comment)
        USING
            'org.apache.cassandra.index.sasi.SASIIndex'
        WITH OPTIONS = """ + """{
            'mode': 'CONTAINS',
            'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.StandardAnalyzer',
            'case_sensitive': 'false'
        }
        """))
        repository.execute(dedent(f"""
        CREATE TABLE IF NOT EXISTS {repository.database}.ENTITY_TEST
        (
            id           text,
            comment      text,
            lucky_number int ,
            is_working   Boolean,

            PRIMARY KEY (id)
        )
        """))
        cls.repository = repository

    def setUp(self) -> None:
        self.repository.execute(f"TRUNCATE TABLE {self.repository.database}.ENTITY_TEST")

    # TEST CASES ----------

    # Test updating a single object from cassandra.
    def test_should_update_cassandra(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        test_entity.comment = 'Updated My-Test Data'
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

    # Test selecting all objects from cassandra.
    def test_should_select_all_from_cassandra(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment='My-Test Data 2', lucky_number=55, is_working=False)
        self.repository.save_all([test_entity_1, test_entity_2])
        result_set = self.repository.find_all()
        self.assertIsNotNone(result_set, "Result set is none")
        expected_list = [test_entity_1, test_entity_2]
        self.assertCountEqual(expected_list, result_set)

    # Test selecting a single object from cassandra.
    def test_should_select_one_from_cassandra(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment='My-Test Data 2', lucky_number=55, is_working=False)
        self.repository.save_all([test_entity_1, test_entity_2])
        result_one = self.repository.find_by_id(test_entity_1.identity)
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity_1.id, result_one.id)
        self.assertEqual(test_entity_1.comment, result_one.comment)
        self.assertEqual(test_entity_1.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_one.is_working)

    # Test deleting one object from cassandra.
    def test_should_delete_from_cassandra(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment='My-Test Data', lucky_number=51, is_working=True)
        self.repository.save(test_entity)
        result_set = self.repository.find_by_id(test_entity.identity)
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertIsInstance(result_set, EntityTest)
        self.assertEqual(test_entity.id, result_set.id)
        self.repository.delete(test_entity)
        result_set = self.repository.find_by_id(test_entity.identity)
        self.assertIsNone(result_set, "Result set is not empty")

    def test_should_select_using_filters(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment='My-Test Data-1', lucky_number=50, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment='My-Work Data-2', lucky_number=40, is_working=False)
        test_entity_3 = EntityTest(Identity.auto(), comment='My-Sets Data-3', lucky_number=30, is_working=True)
        test_entity_4 = EntityTest(Identity.auto(), comment='My-Fest Data-4', lucky_number=20, is_working=False)
        expected_list = [test_entity_1, test_entity_2, test_entity_3, test_entity_4]
        self.repository.save_all(expected_list)
        result_set = self.repository.find_all()
        self.assertCountEqual(expected_list, result_set)
        expected_list = [test_entity_1, test_entity_4]
        result_set = self.repository.find_all(filters=Namespace(by_comment="comment like '%est%'"))
        self.assertCountEqual(expected_list, result_set)
        result_set = self.repository.find_all()
        expected_list = [test_entity_4, test_entity_3, test_entity_2, test_entity_1]
        self.assertCountEqual(expected_list, result_set)


# Program entry point.
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest \
        .TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout) \
        .run(suite)
