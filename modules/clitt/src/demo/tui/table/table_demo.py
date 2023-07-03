#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui.table
      @file: table_demo.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.table.table_renderer import TableRenderer
from hspylib.core.tools.commons import safe_delete_file, sysout

if __name__ == "__main__":
    h = ["string", "number", "boolean", "that`s a big integer column header"]
    data = [("One", 1, True, 2), ("Two", 2, False, 3), ("Three, four and five", 3, True, 3)]
    tr = TableRenderer(h, data, "TableRenderer example of usage")
    tr.adjust_auto_fit()
    tr.set_header_alignment(TableRenderer.TextAlignment.CENTER)
    tr.set_cell_alignment(TableRenderer.TextAlignment.LEFT)
    tr.render()
    tr.export_csv("sample-out.csv")

    sysout('')

    tr2 = TableRenderer.import_csv("sample-out.csv", "TableRenderer example of usage from CVS file")
    tr2.adjust_auto_fit()
    tr2.render()

    safe_delete_file("sample-out.csv")
