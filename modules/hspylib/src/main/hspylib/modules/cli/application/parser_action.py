#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @package: main.modules.cli.application
      @file: argument_chain_builder.py
   @created: hu, 14 Feb 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from hspylib.core.enums.enumeration import Enumeration


class ParserAction(Enumeration):
    """TODO"""

    # @formatter:off

    # This stores a list, and appends each argument value to the list.
    APPEND = 'append'

    # This stores a list, and appends the value specified by the const keyword argument to the list.
    APPEND_CONST = 'append_const'

    # This counts the number of times a keyword argument occurs.
    COUNT = 'count'

    # This just stores the argument’s value.
    STORE = 'store'

    # This stores the value specified by the const keyword argument.
    STORE_CONST = 'store_const'

    # These is a special cases of 'store_const' used for storing True.
    STORE_TRUE = 'store_true'

    # These is a special cases of 'store_const' used for storing False.
    STORE_FALSE = 'store_false'

    # This expects a version= keyword argument, prints version information and exits when invoked.
    VERSION = 'version'

    # @formatter:on

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return str(self)
