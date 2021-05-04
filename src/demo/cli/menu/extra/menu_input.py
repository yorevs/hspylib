#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.demo.cli.menu.extra
      @file: menu_input.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

from hspylib.modules.cli.menu.extra.minput import MenuInput, minput

if __name__ == '__main__':
    # @formatter:off
    form_fields = MenuInput.builder() \
        .field() \
            .label('Letters') \
            .kind('letter') \
            .build() \
        .field() \
            .label('Word') \
            .kind('word') \
            .build() \
        .field() \
            .label('Number') \
            .kind('number') \
            .min_max_length(1, 2) \
            .build() \
        .field() \
            .label('Checkbox') \
            .mode('checkbox') \
            .kind('number') \
            .value('1') \
            .build() \
        .field() \
            .label('Password') \
            .mode('password') \
            .kind('word') \
            .min_max_length(4, 8) \
            .build() \
        .field() \
            .label('Read-Only') \
            .kind('any') \
            .access_type('read-only') \
            .value('READ-ONLY') \
            .build() \
        .build()
    # @formatter:on
    result = minput(form_fields)
    print('\n'.join(map(str, result)))
