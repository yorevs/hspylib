#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   test.tools
      @file: test_text_tools.py
   @created: Thu, 07 Jul 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
import json
import sys
import unittest
from textwrap import dedent

from hspylib.core.tools.text_tools import *


class TestTextTools(unittest.TestCase):
    def test_should_elide_text_if_required(self) -> None:
        text = "1234567890ABCDEFGHIJKLMNOPQRSTUVXYZ"
        elided_text = elide_text(text, 33, "***")
        expected_text = "1234567890ABCDEFGHIJKLMNOPQRST***"
        self.assertEqual(expected_text, elided_text)
        elided_text = elide_text(text, 33)
        expected_text = "1234567890ABCDEFGHIJKLMNOPQRST..."
        self.assertEqual(expected_text, elided_text)

    def test_should_not_elide_text_if_not_required(self) -> None:
        text = "1234567890ABCDEFGHIJKLMNOPQRSTUVXYZ"
        original_text = elide_text(text, 35)
        expected_text = text
        self.assertEqual(expected_text, original_text)

    def test_should_cut_the_string_properly(self) -> None:
        text = "This is just a simple test"
        cut_text, split_parts = cut(text, 3)
        expected_text = "a"
        expected_parts = ("This", "is", "just")
        self.assertEqual(expected_text, cut_text)
        self.assertEqual(expected_parts, split_parts)

    def test_should_not_cut_if_index_is_out_of_bounds(self) -> None:
        text = "This is just a simple test"
        cut_text, split_parts = cut(text, 8)
        self.assertIsNone(cut_text)
        expected_parts = ("This", "is", "just", "a", "simple", "test")
        self.assertEqual(expected_parts, split_parts)

    def test_should_return_a_random_String(self) -> None:
        expected_len = 8
        my_choices = list(string.ascii_lowercase)
        rnd_str_1 = random_string(my_choices, length=expected_len)
        self.assertEqual(len(rnd_str_1), expected_len)
        self.assertTrue(rnd_str_1.islower())
        self.assertTrue(rnd_str_1.isascii())

    def test_should_justify_left(self) -> None:
        text = "simple test"
        ljust_str = justified_left(text, 20, ".")
        expected_text = "simple test........."
        self.assertEqual(expected_text, ljust_str)
        ljust_str = justified_left(text, 20)
        expected_text = "simple test         "
        self.assertEqual(expected_text, ljust_str)

    def test_should_justify_right(self) -> None:
        text = "simple test"
        rjust_str = justified_right(text, 20, ".")
        expected_text = ".........simple test"
        self.assertEqual(expected_text, rjust_str)
        rjust_str = justified_right(text, 20)
        expected_text = "         simple test"
        self.assertEqual(expected_text, rjust_str)

    def test_should_justify_center(self) -> None:
        text = "simple test"
        cjust_str = justified_center(text, 20, ".")
        expected_text = "....simple test....."
        self.assertEqual(expected_text, cjust_str)
        cjust_str = justified_center(text, 20)
        expected_text = "    simple test     "
        self.assertEqual(expected_text, cjust_str)

    def test_should_camel_case(self) -> None:
        text = "This is just a simple test"
        camel_text = camelcase(text)
        expected_text = "thisIsJustASimpleTest"
        self.assertEqual(expected_text, camel_text)
        camel_text_upper = camelcase(text, upper=True)
        expected_text = "ThisIsJustASimpleTest"
        self.assertEqual(expected_text, camel_text_upper)

    def test_should_snake_case(self) -> None:
        text = "This is just a simple test"
        snake_text = snakecase(text)
        expected_text = "this_is_just_a_simple_test"
        self.assertEqual(expected_text, snake_text)
        screaming_snake_text = snakecase(text, screaming=True)
        expected_text = "THIS_IS_JUST_A_SIMPLE_TEST"
        self.assertEqual(expected_text, screaming_snake_text)

    def test_should_kebab_case(self) -> None:
        text = "This is just a simple test"
        kebab_text = kebabcase(text)
        expected_text = "this-is-just-a-simple-test"
        self.assertEqual(kebab_text, expected_text)
        screaming_snake_text = kebabcase(text, train=True)
        expected_text = "THIS-IS-JUST-A-SIMPLE-TEST"
        self.assertEqual(expected_text, screaming_snake_text)

    def test_should_title_case(self) -> None:
        text = "That's not just a simple test"
        titled_text = titlecase(text)
        expected_text = "That's Not Just A Simple Test"
        self.assertEqual(expected_text, titled_text)
        skipped_titled_text = titlecase(text, skip_length=3)
        expected_text = "That's not Just a Simple Test"
        self.assertEqual(expected_text, skipped_titled_text)

    def test_should_convert_between_all_cases(self) -> None:
        text = "This is just a simple test"
        lower_text = lowercase(text)
        expected_text = "this is just a simple test"
        self.assertEqual(expected_text, lower_text)
        upper_text = uppercase(lower_text)
        expected_text = "THIS IS JUST A SIMPLE TEST"
        self.assertEqual(expected_text, upper_text)
        camel_text = camelcase(upper_text)
        expected_text = "thisIsJustASimpleTest"
        self.assertEqual(expected_text, camel_text)
        kebab_text = kebabcase(camel_text)
        expected_text = "this-is-just-a-simple-test"
        self.assertEqual(kebab_text, expected_text)
        snake_text = snakecase(kebab_text)
        expected_text = "this_is_just_a_simple_test"
        self.assertEqual(expected_text, snake_text)
        titled_text = titlecase(kebab_text)
        expected_text = "This Is Just A Simple Test"
        self.assertEqual(expected_text, titled_text)
        original_text = titled_text.capitalize()
        self.assertEqual(text, original_text)

    def test_should_strip_all_escape_codes(self) -> None:
        colored_text = "\x1b[0;msimple test\x1b[0;31m demo"
        stripped_text = strip_escapes(colored_text)
        expected_text = "simple test demo"
        self.assertEqual(expected_text, stripped_text)
        clear_scr_text = "\033[0Hsimple test\033[0J demo"
        stripped_text = strip_escapes(clear_scr_text)
        self.assertEqual(expected_text, stripped_text)
        complex_text = "ls\r\n\x1b[00m\x1b[01;31mexamplefile.zip\x1b[00m\r\n\x1b[01;31m"
        stripped_text = strip_escapes(complex_text)
        expected_text = "ls\r\nexamplefile.zip\r\n"
        self.assertEqual(expected_text, stripped_text)

    def test_should_ensure_endswith(self) -> None:
        text = "this is a test"
        text = ensure_endswith(text, os.linesep)
        self.assertTrue(text.endswith(os.linesep))
        text = ensure_endswith(text, os.linesep)
        self.assertFalse(text.endswith(os.linesep * 2))

    def test_should_ensure_startswith(self) -> None:
        text = "1.0.0"
        text = ensure_startswith(text, "v")
        self.assertTrue(text.startswith("v"))
        text = ensure_startswith(text, "v")
        self.assertFalse(text.startswith("v" * 2))

    def test_should_strip_line_breaks(self) -> None:
        text = "\nThis \ris just \n\ra simple\ttest"
        stripped_text = strip_linebreaks(text)
        expected_text = "This is just a simple\ttest"
        self.assertEqual(expected_text, stripped_text)

    def test_should_strip_extra_spaces(self) -> None:
        text = "   This is  just    a\tsimple      test     "
        stripped_text = strip_extra_spaces(text)
        expected_text = " This is just a simple test "
        self.assertEqual(expected_text, stripped_text)
        stripped_text = strip_extra_spaces(text, trim=True)
        expected_text = "This is just a simple test"
        self.assertEqual(expected_text, stripped_text)

    def test_should_json_stringify(self) -> None:
        dict_test = {"a": "val_a", "b": 1, "c": True, "d": {"d1": 0, "d2": "1"}}
        dumped = json.dumps(dict_test, indent=2)
        json_string = '{"collection": "' + json_stringify(dumped) + '"}'
        json_obj = json.loads(json_string)
        self.assertIsNotNone(json_obj)
        self.assertTrue("collection" in json_obj)
        self.assertTrue(isinstance(json_obj["collection"], str))
        original = json.loads(json_obj["collection"])
        self.assertIsNotNone(original)
        self.assertEqual(original["a"], "val_a")
        self.assertEqual(original["b"], 1)
        self.assertTrue(original["c"])
        self.assertEqual(original["d"], {"d1": 0, "d2": "1"})

    def test_should_append_correct_eols(self) -> None:
        text = os.linesep
        for i in range(0, 11):
            text += str(i) + eol(i, 3)
        expected_text = dedent(
            """
            0 1 2
            3 4 5
            6 7 8
            9 10 """
        )
        self.assertEqual(expected_text, text)

    def test_should_quote_only_strings(self) -> None:
        str_value_1 = "This is just"
        str_value_2 = "a simple test"
        quoted = quote(str_value_1) + " " + quote(str_value_2)
        expected_text = "'This is just' 'a simple test'"
        self.assertEqual(expected_text, quoted)
        expected_text = "'This is just' :True :1 :1.0 'a simple test'"
        quoted = f"{quote(str_value_1)} :{quote(True)} :{quote(1)} :{quote(1.0)} {quote(str_value_2)}"
        self.assertEqual(expected_text, quoted)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextTools)
    unittest.TextTestRunner(verbosity=2, failfast=True, stream=sys.stdout).run(suite)
