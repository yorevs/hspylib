#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   test.modules.json_search
      @file: test_json_search.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from os import path

import json
import os
import sys
import unittest

from hspylib.core.tools.json_search import JsonSearch

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

SAMPLE_FILE = f"{TEST_DIR}/resources/json_search_sample.json"


class TestJsonSearch(unittest.TestCase):

    # Setup tests
    def setUp(self):
        self.assertTrue(path.exists(SAMPLE_FILE), "Sample file was not found on {}".format(SAMPLE_FILE))
        with open(SAMPLE_FILE) as f_sample_file:
            self.json_object = json.load(f_sample_file)
            self.j_utils = JsonSearch()

    # TEST CASES ----------

    # TC1 - Test selecting a simple element.
    def test_should_select_a_simple_element(self):
        st = self.j_utils.select(self.json_object, "elem0")
        self.assertIsNone(st)
        st = self.j_utils.select(self.json_object, "elem1")
        self.assertEqual("value1", st)

    # TC2 - Test selecting a nested element.
    def test_should_select_a_nested_element(self):
        st = self.j_utils.select(self.json_object, "elem2.elem2_1")
        self.assertEqual("value2_1", st)
        st = self.j_utils.select(self.json_object, "elem2.elem2_3.elem2_3_2")
        self.assertEqual("value2_3_2", st)

    # TC3 - Test selecting an indexed element.
    def test_should_select_an_indexed_element(self):
        st = self.j_utils.select(self.json_object, "elem3[0]")
        self.assertEqual({"name1": "value_name1"}, st)
        st = self.j_utils.select(self.json_object, "elem3[2]")
        self.assertEqual({"name3": [{"inner_name1": "inner_value1"}, {"inner_name1": "inner_value2"}]}, st)

    # TC4 - Test selecting a nested indexed element.
    def test_should_select_a_nested_indexed_element(self):
        st = self.j_utils.select(self.json_object, "elem3[2].name3")
        self.assertEqual([{"inner_name1": "inner_value1"}, {"inner_name1": "inner_value2"}], st)
        st = self.j_utils.select(self.json_object, "elem3[2].name3[0]")
        self.assertEqual({"inner_name1": "inner_value1"}, st)
        st = self.j_utils.select(self.json_object, "elem3[2].name3[0].inner_name1")
        self.assertEqual("inner_value1", st)

    # TC5 - Test selecting a nested element by a property value inside an options.
    def test_should_select_a_nested_element_by_a_property_value_inside_array(self):
        st = self.j_utils.select(self.json_object, "elem5{radio}")
        self.assertEqual("Gaga", st)
        st = self.j_utils.select(self.json_object, "elem5{radio<Gugo>}")
        self.assertEqual("Gugo", st)

    # TC6 - Test selecting a nested property nested inside an options by a property value inside an options.
    def test_should_select_a_nested_property_nested_inside_array_by_a_property_value_inside_array(self):
        st = self.j_utils.select(self.json_object, "elem4{elem4_1}{elem4_1_1}{inner_nested_name1}")
        self.assertEqual("inner_nested_value1_1", st)
        st = self.j_utils.select(
            self.json_object, "elem4{elem4_1}{elem4_1_1}{inner_nested_name1<inner_nested_value2_1>}"
        )
        self.assertEqual("inner_nested_value2_1", st)
        st = self.j_utils.select(
            self.json_object, "elem4{elem4_1}{elem4_1_2}{inner_nested_name1<inner_nested_value4_1>}"
        )
        self.assertEqual("inner_nested_value4_1", st)

    # TC7 - Test selecting mixed nested properties and indexes.
    def test_select_mixed_nested_properties_and_indexes(self):
        st = self.j_utils.select(
            self.json_object, "elem4{elem4_2}[0].elem4_2_1{inner_nested_name1<inner_nested_value2_1>}"
        )
        self.assertEqual("inner_nested_value2_1", st)
        st = self.j_utils.select(
            self.json_object, "elem4{elem4_2}[1].elem4_2_2{inner_nested_name1<inner_nested_value4_1>}"
        )
        self.assertEqual("inner_nested_value4_1", st)

    # TC8 - Test selecting parents.
    def test_should_select_parents(self):
        st = self.j_utils.select(self.json_object, "elem6.elem6_1.{elem6_1_1<value6_1_1_B>}", True)
        self.assertEqual(
            {
                "elem6_1_1": "value6_1_1_B",
                "elem6_1_2": "value6_1_2_B",
                "elem6_1_3": [
                    {"elem6_1_3_1": "value6_1_3_1_B", "elem6_1_3_2": "value6_1_3_2_B"},
                    {"elem6_1_3_1": "value6_1_3_1_D", "elem6_1_3_2": "value6_1_3_2_D"},
                ],
            },
            st,
        )
        st = self.j_utils.select(self.json_object, "elem6.elem6_1.{elem6_1_1<value6_1_1_A>}", True)
        self.assertEqual(
            {
                "elem6_1_1": "value6_1_1_A",
                "elem6_1_2": "value6_1_2_A",
                "elem6_1_3": [
                    {"elem6_1_3_1": "value6_1_3_1_A", "elem6_1_3_2": "value6_1_3_2_A"},
                    {"elem6_1_3_1": "value6_1_3_1_C", "elem6_1_3_2": "value6_1_3_2_C"},
                ],
            },
            st,
        )
        st = self.j_utils.select(
            self.json_object, "elem6.elem6_1.{elem6_1_1<value6_1_1_A>}.elem6_1_3{elem6_1_3_1<value6_1_3_1_A>}", True
        )
        self.assertEqual({"elem6_1_3_1": "value6_1_3_1_A", "elem6_1_3_2": "value6_1_3_2_A"}, st)


# Program entry point.
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJsonSearch)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
