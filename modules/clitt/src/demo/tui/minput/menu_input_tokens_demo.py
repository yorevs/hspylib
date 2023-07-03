#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui.minput
      @file: menu_input_tokens_demo.py
   @created: Fri, 30 May 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.minput.menu_input import MenuInput
from clitt.core.tui.minput.minput import minput

if __name__ == "__main__":
    tokens = [
        "Name|||5/30|rw|",
        "Age||numbers|1/3||",
        "Password|password||5|rw|",
        "Masked|masked|||rw|;##.## @ x",
        "Role|select|||rw|Admin;<User>;Guest",
        "Locked||||r|locked value",
        "Accept Conditions|checkbox||||",
    ]
    form_fields = MenuInput.builder().from_tokenized(tokens).build()
    result = minput(form_fields)
    print(result if result else "None")
