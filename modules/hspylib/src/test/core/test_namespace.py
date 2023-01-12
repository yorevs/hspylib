#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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

    def test_should_return_all_attributes_and_values(self) -> None:
        ns = Namespace.of("TestNs", {"name": "John", "age": 44, "active": True, "nested": {"n1": 1, "n2": 2}})
        self.assertEqual(4, len(ns))
        expected_attrs = ["name", "age", "active", "nested"]
        expected_vals = ["John", 44, True, {"n1": 1, "n2": 2}]
        self.assertCountEqual(expected_attrs, ns.attributes)
        self.assertCountEqual(expected_vals, ns.values)

    def test_should_not_allow_forbidden_attribute_names(self) -> None:
        with self.assertRaises(Exception) as context:
            Namespace("TestNs", items="John")
            self.assertTrue(NameError, type(context.exception))
            self.assertTrue("Invalid attribute name" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Namespace("TestNs", _name="John")
            self.assertTrue(NameError, type(context.exception))
            self.assertTrue("Invalid attribute name" in str(context.exception))
        with self.assertRaises(Exception) as context:
            Namespace("TestNs", __name__="John")
            self.assertTrue(NameError, type(context.exception))
            self.assertTrue("Invalid attribute name" in str(context.exception))

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
        self.assertTrue("name" in ns)
        self.assertTrue("age" in ns)
        self.assertTrue("active" in ns)
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
        self.assertEqual("TestNs_SubNs", ns.__name__)

    def test_should_not_allow_modify_final(self) -> None:
        ns = Namespace("TestNs", True, name="John", age=44)
        self.assertTrue(ns.hasattr("name"))
        self.assertTrue(ns.hasattr("age"))
        self.assertRaisesRegex(
            ValueError, "Can't set attribute 'active'. 'TestNs' Namespace is final",
            lambda: ns.setattr("active", True)
        )

    def test_should_return_namespace_as_dictionary(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True) + Namespace("SubNs", add=True)
        dict_ns = ns._asdict()
        self.assertTrue(isinstance(dict_ns, dict))
        self.assertFalse("_final" in dict_ns)
        self.assertFalse("_index" in dict_ns)
        self.assertTrue("name" in dict_ns)
        self.assertTrue("age" in dict_ns)
        self.assertTrue("active" in dict_ns)
        self.assertTrue("add" in dict_ns)

    def test_should_convert_to_String(self) -> None:
        ns = Namespace("TestNs", name="John", age=44, active=True) + Namespace("SubNs", add=True)
        expected_string = "TestNs_SubNs(name=John, age=44, active=True, add=True)"
        self.assertEqual(expected_string, str(ns))
        self.assertEqual(expected_string, repr(ns))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNamespace)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
