#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.cli.tui.extra
      @file: menu_input.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""
from hspylib.modules.cli.tui.extra.minput.input_validator import InputValidator
from hspylib.modules.cli.tui.extra.minput.minput import MenuInput, minput

if __name__ == '__main__':
    # @formatter:off
    form_fields = MenuInput.builder() \
        .field() \
            .label('letters') \
            .validator(InputValidator.letters()) \
            .build() \
        .field() \
            .label('word') \
            .validator(InputValidator.words()) \
            .build() \
        .field() \
            .label('number') \
            .validator(InputValidator.numbers()) \
            .min_max_length(1, 2) \
            .build() \
        .field() \
            .label('masked') \
            .itype('masked') \
            .value('|##::##::## @@') \
            .build() \
        .field() \
            .label('selectable') \
            .itype('select') \
            .value('one|two|three') \
            .build() \
        .field() \
            .label('checkbox') \
            .itype('checkbox') \
            .build() \
        .field() \
            .label('password') \
            .itype('password') \
            .validator(InputValidator.anything()) \
            .min_max_length(4, 8) \
            .build() \
        .field() \
            .label('read-only') \
            .access_type('read-only') \
            .value('READ-ONLY') \
            .build() \
        .build()
    # @formatter:on
    result = minput(form_fields)
    print(result.__dict__)
