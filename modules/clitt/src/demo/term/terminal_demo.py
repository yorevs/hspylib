#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.term
      @file: terminal_demo.py
   @created: Fri, 7 Jul 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.term.commons import get_cursor_position
from clitt.core.term.terminal import Terminal

if __name__ == '__main__':
    t = Terminal.INSTANCE
    Terminal.echo("Hello terminal!", end='')
    Terminal.echo(get_cursor_position(), end='')
    Terminal.echo(t.cursor, end='')
