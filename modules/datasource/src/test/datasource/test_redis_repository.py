#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Datasource
   @package: test.datasource
      @file: test_mysql_repository.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

import logging as log
import os
import sys
import unittest
from hspylib.core.decorator.decorators import integration_test
from hspylib.core.tools.commons import log_init

from datasource.identity import Identity
from datasource.redis.redis_configuration import RedisConfiguration
from shared.entity_test import EntityTest
from shared.redis_repository_test import RedisRepositoryTest

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


@integration_test
class TestClass(unittest.TestCase):
    """
    Docker command:
    $ docker run --rm -d --name some-redis -p 6379:6379
        -e REDIS_ARGS="--requirepass password" redis/redis-stack-server:latest
    """

    # Setup tests
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["DATASOURCE_PORT"] = "6379"
        os.environ["DATASOURCE_PASSWORD"] = "password"
        log_init(file_enable=False, console_enable=True)
        resource_dir = "{}/resources".format(TEST_DIR)
        config = RedisConfiguration(resource_dir, profile="test")
        log.info(config)
        cls.repository = RedisRepositoryTest(config)

    def setUp(self) -> None:
        self.repository.flushdb()

    # TEST CASES ----------

    # Test updating a single row from the database.
    def test_should_update_redis_database(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.set(test_entity)
        test_entity.comment = "Updated My-Test Data"
        self.repository.set(test_entity)
        result_set = self.repository.mget(self.repository.build_key(test_entity))
        self.assertIsNotNone(result_set, "Result set is none")
        self.assertEqual(1, len(result_set))
        result_one = result_set[0]
        self.assertEqual(test_entity.id, result_one.id)
        self.assertEqual(test_entity.comment, result_one.comment)
        self.assertEqual(test_entity.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity.is_working, result_one.is_working)

    # Test selecting all objects from the database.
    def test_should_select_all_from_redis(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.set(test_entity_1, test_entity_2)
        result_set = self.repository.mget(test_entity_1.key(), test_entity_2.key())
        self.assertIsNotNone(result_set, "Result set is none")
        expected_list = [test_entity_1, test_entity_2]
        self.assertCountEqual(expected_list, result_set)

    # Test selecting a single row from the database.
    def test_should_select_one_from_postgres(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.set(test_entity_1, test_entity_2)
        result_one = self.repository.get(test_entity_1.key())
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity_1.id, result_one.id)
        self.assertEqual(test_entity_1.comment, result_one.comment)
        self.assertEqual(test_entity_1.lucky_number, result_one.lucky_number)
        self.assertEqual(test_entity_1.is_working, result_one.is_working)

    # Test deleting one row from the database.
    def test_should_delete_from_postgres(self) -> None:
        test_entity = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        self.repository.set(test_entity)
        result_one = self.repository.get(test_entity.key())
        self.assertIsNotNone(result_one, "Result set is none")
        self.assertIsInstance(result_one, EntityTest)
        self.assertEqual(test_entity.id, result_one.id)
        self.repository.delete(test_entity.key())
        result_one = self.repository.get(test_entity.key())
        self.assertIsNone(result_one, "Result set is not empty")

    # Test get redis keys by pattern
    def test_should_fetch_redis_keys(self) -> None:
        test_entity_1 = EntityTest(Identity.auto(), comment="My-Test Data", lucky_number=51, is_working=True)
        test_entity_2 = EntityTest(Identity.auto(), comment="My-Test Data 2", lucky_number=55, is_working=False)
        self.repository.set(test_entity_1, test_entity_2)
        expected_keys = [test_entity_1.key(), test_entity_2.key()]
        result_set = self.repository.keys("ENTITY_TEST_ID_*")
        self.assertCountEqual(expected_keys, result_set)


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
