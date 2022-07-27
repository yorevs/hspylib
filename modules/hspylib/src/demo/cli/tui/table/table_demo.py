#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   demo.cli.table
      @file: table_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.modules.cli.tui.table.table_renderer import TableRenderer

if __name__ == '__main__':
    h = [
        'String',
        'Number',
        'Boolean',
        'That`s a big Integer Column Header'
    ]
    data = [
        ('One', 1, True, 2),
        ('Two', 2, False, 3),
        ('Three, four and five', 3, True, 3),
    ]
    tr = TableRenderer(h, data, 'TableRenderer example of usage')
    tr.adjust_sizes_by_largest_cell()
    tr.set_header_alignment(TableRenderer.TextAlignment.CENTER)
    tr.set_cell_alignment(TableRenderer.TextAlignment.LEFT)
    tr.render()
