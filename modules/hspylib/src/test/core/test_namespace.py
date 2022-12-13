#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.tools
      @file: test_namespace.py
   @created: Thu, 03 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
from hspylib.core.namespace import Namespace

import sys
import unittest


class TestNamespace(unittest.TestCase):
    def test_should_not_allow_private_or_protected_attribute_names(self) -> None:
        with self.assertRaises(Exception) as context:
            Namespace("TestNs", _name="John", age=44, active=True)
        self.assertTrue(NameError, type(context.exception))
        self.assertTrue("Attribute names can't start with '_' or '__'" in str(context.exception))

    def test_len_should_return_the_numer_of_attributes(self) -> None:
        ns = Namespace.of("TestNs", {"name": "John", "age": 44, "active": True, "nested": {"n1": 1, "n2": 2}})
        self.assertEqual(4, len(ns))
        expected_attrs = ["name", "age", "active", "nested"]
        self.assertCountEqual(expected_attrs, ns.attributes)

    def test_should_create_namespace_from_kwargs(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True)
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertTrue(ns.hasattr("active"))
        self.assertEqual("John", ns.name)
        self.assertEqual(44, ns.age)
        self.assertEqual(True, ns.active)

    def test_should_create_namespace_from_dict(self) -> None:
        ns = Namespace.of("TestNs", {"name": "John", "age": 44, "active": True, "nested": {"n1": 1, "n2": 2}})
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertTrue(ns.hasattr("active"))
        self.assertTrue(ns.hasattr("nested"))
        self.assertTrue("n1" in ns.nested)
        self.assertTrue("n2" in ns.nested)
        self.assertEqual("John", ns.name)
        self.assertEqual(44, ns.age)
        self.assertEqual(True, ns.active)
        self.assertEqual(1, ns.nested["n1"])
        self.assertEqual(2, ns.nested["n2"])

    def test_should_create_namespace_from_list_of_dicts(self) -> None:
        ns = Namespace.of("TestNs", [{"name": "John", "nested": {"n1": 1, "n2": 2}}, {"age": 44, "active": True}])
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertTrue(ns.hasattr("active"))
        self.assertTrue(ns.hasattr("nested"))
        self.assertTrue("n1" in ns.nested)
        self.assertTrue("n2" in ns.nested)
        self.assertEqual("John", ns.name)
        self.assertEqual(44, ns.age)
        self.assertEqual(True, ns.active)
        self.assertEqual(1, ns.nested["n1"])
        self.assertEqual(2, ns.nested["n2"])

    def test_should_be_iterable(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True)
        expected = [("name", "John"), ("age", 44), ("active", True)]
        for n in ns:
            self.assertTrue(n in expected)

    def test_should_be_iterable_with_items(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True)
        expected = [("name", "John"), ("age", 44), ("active", True)]
        self.assertTrue(all((k, v) in expected for k, v in ns.items()))

    def test_should_return_dict(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True)
        expected = {"__name__": "TestNs", "_index": 0, "_final": False, "name": "John", "age": 44, "active": True}
        self.assertEqual(expected, ns.__dict__)

    def test_should_override_add(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True)
        ns += Namespace("SubNs", add=True)
        ns += {"sub_dict": True}
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertTrue(ns.hasattr("active"))
        self.assertTrue(ns.hasattr("add"))
        self.assertTrue(ns.hasattr("sub_dict"))
        self.assertEqual("John", ns.name)
        self.assertEqual(44, ns.age)
        self.assertEqual(True, ns.add)
        self.assertEqual(True, ns.sub_dict)
        self.assertEqual("TestNs", ns.__name__)

    def test_should_override_iadd(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True) + Namespace("SubNs", add=True)
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertTrue(ns.hasattr("active"))
        self.assertTrue(ns.hasattr("add"))
        self.assertEqual("John", ns.name)
        self.assertEqual(44, ns.age)
        self.assertEqual(True, ns.add)
        self.assertEqual("TestNs.SubNs", ns.__name__)

    def test_should_not_allow_modify_final(self) -> None:
        ns = Namespace("TestNs", True, name="John", age=44)
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertRaisesRegex(ValueError, "TestNs Namespace is final", lambda: ns.setattr("active", True))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNamespace)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
