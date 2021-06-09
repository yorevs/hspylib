#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   hspylib.demo.calculator.ui.qt.views
      @file: main_qt_view.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2021, HSPyLib team
"""

import logging as log

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLCDNumber, QWidget, QToolButton

from calculator.core.enums.calc_operations import CalcOperations
from calculator.ui.qt.views.blink_lcd_thread import BlinkLcdThread
from hspylib.core.config.app_config import AppConfigs
from hspylib.modules.qt.views.qt_view import QtView


class MainQtView(QtView):

    def __init__(self):
        form, window = QtView.load_ui_form('qt_calculator.ui')
        # Must come after the initialization above
        super().__init__(form, window)
        self.configs = AppConfigs.INSTANCE
        self.dec_sep = AppConfigs.INSTANCE['decimal.separator']
        self.min_digits = int(AppConfigs.INSTANCE['min.digits'])
        self.max_digits = int(AppConfigs.INSTANCE['max.digits'])
        self.wait_operand = True
        self.wait_operand2 = True
        self.operand = None
        self.operand2 = None
        self.last_operand = None
        self.memory_rec = None
        self.display_text = ''
        self.op = CalcOperations.NO_OP
        # Find Qt components {
        self.frameMain = self.qt_finder.find_widget(QWidget, 'frameMain')
        self.lcdDisplay = self.qt_finder.find_widget(QLCDNumber, 'lcdDisplay')
        self.btnAC = self.qt_finder.find_widget(QToolButton, 'btnAC')
        self.btnSignal = self.qt_finder.find_widget(QToolButton, 'btnSignal')
        self.btnPercent = self.qt_finder.find_widget(QToolButton, 'btnPercent')
        self.btnDivision = self.qt_finder.find_widget(QToolButton, 'btnDivision')
        self.btn7 = self.qt_finder.find_widget(QToolButton, 'btn7')
        self.btn8 = self.qt_finder.find_widget(QToolButton, 'btn8')
        self.btn9 = self.qt_finder.find_widget(QToolButton, 'btn9')
        self.btnMultiplication = self.qt_finder.find_widget(QToolButton, 'btnMultiplication')
        self.btn4 = self.qt_finder.find_widget(QToolButton, 'btn4')
        self.btn5 = self.qt_finder.find_widget(QToolButton, 'btn5')
        self.btn6 = self.qt_finder.find_widget(QToolButton, 'btn6')
        self.btnMinus = self.qt_finder.find_widget(QToolButton, 'btnMinus')
        self.btn1 = self.qt_finder.find_widget(QToolButton, 'btn1')
        self.btn2 = self.qt_finder.find_widget(QToolButton, 'btn2')
        self.btn3 = self.qt_finder.find_widget(QToolButton, 'btn3')
        self.btnPlus = self.qt_finder.find_widget(QToolButton, 'btnPlus')
        self.btn0 = self.qt_finder.find_widget(QToolButton, 'btn0')
        self.btnDecimal = self.qt_finder.find_widget(QToolButton, 'btnDecimal')
        self.btnEqual = self.qt_finder.find_widget(QToolButton, 'btnEqual')
        # }
        self.setup_ui()

    def setup_ui(self):
        """Connect signals and startup components"""
        self.btnAC.clicked.connect(self._btn_ac_clicked)
        self.btnSignal.clicked.connect(self._btn_signal_clicked)
        self.btnPercent.clicked.connect(self._btn_percent_clicked)
        self.btnDivision.clicked.connect(self._btn_division_clicked)
        self.btn7.clicked.connect(self._btn7_clicked)
        self.btn8.clicked.connect(self._btn8_clicked)
        self.btn9.clicked.connect(self._btn9_clicked)
        self.btnMultiplication.clicked.connect(self._btn_times_clicked)
        self.btn4.clicked.connect(self._btn4_clicked)
        self.btn5.clicked.connect(self._btn5_clicked)
        self.btn6.clicked.connect(self._btn6_clicked)
        self.btnMinus.clicked.connect(self._btn_minus_clicked)
        self.btn1.clicked.connect(self._btn1_clicked)
        self.btn2.clicked.connect(self._btn2_clicked)
        self.btn3.clicked.connect(self._btn3_clicked)
        self.btnPlus.clicked.connect(self._btn_plus_clicked)
        self.btn0.clicked.connect(self._btn0_clicked)
        self.btnDecimal.clicked.connect(self._btn_comma_clicked)
        self.btnDecimal.setText(self.dec_sep)
        self.btnEqual.clicked.connect(self._btn_equal_clicked)
        self.frameMain.keyPressed.connect(self._key_pressed)

    def _key_pressed(self, key_pressed):
        if Qt.Key_1 == key_pressed:
            self._btn1_clicked()
        elif Qt.Key_2 == key_pressed:
            self._btn2_clicked()
        elif Qt.Key_3 == key_pressed:
            self._btn3_clicked()
        elif Qt.Key_4 == key_pressed:
            self._btn4_clicked()
        elif Qt.Key_5 == key_pressed:
            self._btn5_clicked()
        elif Qt.Key_6 == key_pressed:
            self._btn6_clicked()
        elif Qt.Key_7 == key_pressed:
            self._btn7_clicked()
        elif Qt.Key_8 == key_pressed:
            self._btn8_clicked()
        elif Qt.Key_9 == key_pressed:
            self._btn9_clicked()
        elif Qt.Key_0 == key_pressed:
            self._btn0_clicked()
        elif Qt.Key_Plus == key_pressed:
            self._btn_plus_clicked()
        elif Qt.Key_Minus == key_pressed:
            self._btn_minus_clicked()
        elif Qt.Key_Slash == key_pressed:
            self._btn_division_clicked()
        elif Qt.Key_Percent == key_pressed:
            self._btn_percent_clicked()
        elif key_pressed in [Qt.Key_Equal, Qt.Key_Return]:
            self._btn_equal_clicked()
        elif Qt.Key_Backspace == key_pressed:
            self._remove_digit()
        elif key_pressed in [Qt.Key_Period, Qt.Key_Comma]:
            self._btn_signal_clicked()
        elif Qt.Key_Escape == key_pressed:
            self._btn_ac_clicked()

    def _display(self, value):
        future_digits = len(str(value)) if value else 0
        digits = self.lcdDisplay.digitCount()
        if future_digits > digits:
            self.lcdDisplay.setDigitCount(min(future_digits, self.max_digits))
        elif future_digits <= digits:
            self.lcdDisplay.setDigitCount(max(future_digits, self.min_digits))
        self.lcdDisplay.display(value)

    def _blink_lcd(self):
        blink = BlinkLcdThread(self.lcdDisplay)
        blink.start()
        self.display_text = ''

    def _soft_reset(self):
        self.wait_operand = True
        self.wait_operand2 = True
        self.last_operand = self.operand2
        self.operand = 0
        self.operand2 = 0
        self.memory_rec = 0
        self.display_text = ''

    def _append_digit(self, digit: int):
        self.btnAC.setText('C')
        if not self.display_text or self.display_text == '0':
            self.display_text = str(digit)
        else:
            self.display_text += str(digit)
        self._display(self.display_text)

    def _remove_digit(self):
        if not self.display_text:
            return
        if len(self.display_text) <= 1:
            self._btn_ac_clicked()
            return
        self.display_text = self.display_text[:-1]
        self._display(self.display_text)

    def _calculate(self):
        result = 0
        if not self.op or not self.operand:
            return

        if self.op == CalcOperations.SUM:
            result = self.operand + self.operand2
        elif self.op == CalcOperations.SUBTRACTION:
            result = self.operand - self.operand2
        elif self.op == CalcOperations.MULTIPLICATION:
            result = self.operand * self.operand2
        elif self.op == CalcOperations.DIVISION:
            if self.operand2 == 0:
                result = 'oo'
            else:
                result = self.operand / self.operand2
        self._display(result)
        self.memory_rec = 0

    def _change_op(self, op: CalcOperations):
        self.op = op
        if self.wait_operand:
            self.operand = self.lcdDisplay.value()
            self.memory_rec = self.operand
            self.wait_operand = False
        elif self.wait_operand2:
            self.operand2 = self.lcdDisplay.value()
            self.wait_operand2 = False
        if not self.wait_operand and not self.wait_operand2:
            self._calculate()
            self.operand = self.lcdDisplay.value()
            self.wait_operand2 = True
        self._blink_lcd()

    def _btn_equal_clicked(self):
        log.info("Clicked: =")
        if self.wait_operand:
            self.operand = self.lcdDisplay.value()
            self.operand2 = self.last_operand if self.last_operand else None
        elif self.wait_operand2:
            self.operand2 = self.lcdDisplay.value()
        if self.operand and self.operand2:
            self._calculate()
        self._soft_reset()
        self._blink_lcd()

    def _btn_ac_clicked(self):
        log.info("Clicked: AC")
        if self.memory_rec:
            self.memory_rec = 0
        else:
            self.lcdDisplay.setDigitCount(self.min_digits)
            self._display(0)
            self._soft_reset()
            self.btnAC.setText('AC')
        self.display_text = ''
        self._blink_lcd()

    def _btn_signal_clicked(self):
        log.info("Clicked: +-")
        self._display(self.lcdDisplay.value() * -1)
        self.display_text = str(self.lcdDisplay.value())

    def _btn_percent_clicked(self):
        log.info("Clicked: %")
        if not self.memory_rec:
            self._display(self.lcdDisplay.value() / 100)
            self.display_text = ''
        else:
            operand1 = self.memory_rec
            operand2 = self.lcdDisplay.value()
            self._display(operand1 * (operand2 / 100))
            self.display_text = str(self.lcdDisplay.value())
            self.memory_rec = self.lcdDisplay.value()

    def _btn_division_clicked(self):
        log.info("Clicked: /")
        self._change_op(CalcOperations.DIVISION)

    def _btn7_clicked(self):
        log.info("Clicked: 7")
        self._append_digit(7)

    def _btn8_clicked(self):
        log.info("Clicked: 8")
        self._append_digit(8)

    def _btn9_clicked(self):
        log.info("Clicked: 9")
        self._append_digit(9)

    def _btn_times_clicked(self):
        log.info("Clicked: x")
        self._change_op(CalcOperations.MULTIPLICATION)

    def _btn4_clicked(self):
        log.info("Clicked: 4")
        self._append_digit(4)

    def _btn5_clicked(self):
        log.info("Clicked: 5")
        self._append_digit(5)

    def _btn6_clicked(self):
        log.info("Clicked: 6")
        self._append_digit(6)

    def _btn_minus_clicked(self):
        log.info("Clicked: -")
        self._change_op(CalcOperations.SUBTRACTION)

    def _btn1_clicked(self):
        log.info("Clicked: 1")
        self._append_digit(1)

    def _btn2_clicked(self):
        log.info("Clicked: 2")
        self._append_digit(2)

    def _btn3_clicked(self):
        log.info("Clicked: 3")
        self._append_digit(3)

    def _btn_plus_clicked(self):
        log.info("Clicked: +")
        self._change_op(CalcOperations.SUM)

    def _btn0_clicked(self):
        log.info("Clicked: 0")
        self._append_digit(0)

    def _btn_comma_clicked(self):
        log.info("Clicked: ,")
        if self.dec_sep not in self.display_text:
            self.display_text += self.dec_sep if self.display_text else '0' + self.dec_sep
        self._display(self.display_text)
