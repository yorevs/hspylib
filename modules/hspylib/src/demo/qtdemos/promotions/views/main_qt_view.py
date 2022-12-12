#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
      @file: main_qt_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""

from hspylib.core.config.app_config import AppConfigs
from hspylib.modules.qt.promotions.htablemodel import HTableModel
from hspylib.modules.qt.views.qt_view import QtView
from qtdemos.promotions.core.demo_table_row import DemoTableRow


class MainQtView(QtView):
    """TODO"""

    UI_FILE = 'qt_promotions.ui'

    def __init__(self):
        super().__init__(self.UI_FILE)
        self.configs = AppConfigs.INSTANCE
        self.tbl_model = HTableModel(self.ui.tbl_htable_view, DemoTableRow)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Connect signals and startup components"""
        self.ui.btn_next.clicked.connect(self.ui.stk_hstacked_widget.slide_next)
        self.ui.btn_prev.clicked.connect(self.ui.stk_hstacked_widget.slide_previous)
        self.ui.btn_submit.clicked.connect(self.submit)
        self.ui.lst_hlist_widget.set_editable(True)
        self.ui.te_hconsole.set_highlight_enable(True)
        self.ui.te_hconsole.set_show_line_numbers(True)
        self.ui.te_hconsole.setReadOnly(False)
        self.ui.lbl_status.set_clickable(True)
        self.ui.lbl_status.set_dynamic_tooltip(True)
        self.ui.lbl_status.clicked.connect(lambda: print('Clicked status: ' + self.ui.lbl_status.text()))

    def submit(self) -> None:
        """TODO"""
        row = DemoTableRow(self)
        row.color = self.ui.cmb_hcombo_box.currentText()
        row.text = self.ui.le_hline_edit.text()
        row.desc = self.ui.te_hconsole.toPlainText()
        row.lst_items = self.ui.lst_hlist_widget.as_list()
        self.tbl_model.push_data(row)
        self.ui.lbl_status.setText(f'Record added: {str(row)}')
        self.ui.stk_hstacked_widget.slide_to_index(0)
