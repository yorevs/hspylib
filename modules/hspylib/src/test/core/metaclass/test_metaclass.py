#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: hspylib
   @package: hspylib.test.core.metaclass
      @file: test_metaclass.py
   @created: Sat, 12 Nov 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

import sys
import unittest
from abc import abstractmethod

from hspylib.core.exception.exceptions import HSBaseException
from hspylib.core.metaclass.singleton import AbstractSingleton, Singleton


class TestClass(unittest.TestCase):
    class SingletonClass(metaclass=Singleton):
        pass

    class MessySingleton(metaclass=Singleton):
        def __init__(self):
            raise Exception("Test exception")

    class AbstractSingletonClass(metaclass=AbstractSingleton):
        @abstractmethod
        def do_it(self) -> int:
            """Abstract method"""

    class ConcreteSingletonClass(AbstractSingletonClass):
        def do_it(self) -> int:
            print("Done")
            return 1

    # TEST CASES ----------

    # Test singletons are the same instance.
    def test_singleton_should_be_singleton(self) -> None:
        self.assertFalse(Singleton.has_instance(TestClass.SingletonClass))
        instance_1 = TestClass.SingletonClass()
        self.assertTrue(Singleton.has_instance(TestClass.SingletonClass))
        instance_2 = TestClass.SingletonClass()
        self.assertEqual(instance_1, instance_2)
        self.assertEqual(hash(instance_1), hash(instance_2))

    # Test raised exceptions are properly wrapped into HSBaseException
    def test_singleton_creation_with_error_should_re_raise_wrapped_exception(self) -> None:
        expected_msg = "### Failed to create singleton instance: 'MessySingleton'"
        lm = len(expected_msg)
        with self.assertRaises(HSBaseException) as cm:
            TestClass.MessySingleton()
        self.assertEqual(expected_msg, str(cm.exception)[:lm])

    def test_should_not_allow_instantiate_abstract_singleton(self) -> None:
        expected_msg = "Can't instantiate abstract class AbstractSingletonClass with abstract method do_it"
        with self.assertRaises(HSBaseException) as cm:
            TestClass.AbstractSingletonClass()
        self.assertIn(expected_msg, str(cm.exception))

    def test_should_allow_instantiate_concrete_singleton(self) -> None:
        t = TestClass.ConcreteSingletonClass()
        self.assertEqual(1, t.do_it())


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
