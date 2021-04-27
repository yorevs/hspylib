import logging as log
from threading import Thread
from time import sleep

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtWidgets import QWidget

from calculator.core.enum.calc_operations import CalcOperations
from hspylib.core.config.app_config import AppConfigs
from hspylib.ui.qt.views.qt_view import QtView


class MainView(QtView):

    class BlinkLcdThread(Thread):
        def __init__(self, lcd: QLCDNumber):
            Thread.__init__(self)
            self.lcd = lcd

        def run(self):
            palette = self.lcd.palette()
            fg_color = palette.color(palette.WindowText)
            bg_color = palette.color(palette.Background)
            palette.setColor(palette.WindowText, bg_color)
            self.lcd.setPalette(palette)
            sleep(float(AppConfigs.INSTANCE['lcd.blink.delay']))
            palette.setColor(palette.WindowText, fg_color)
            self.lcd.setPalette(palette)

    def __init__(self):
        form, window = uic \
            .loadUiType("{}/forms/qt_calculator.ui".format(AppConfigs.INSTANCE.resource_dir()))
        super().__init__(window())
        self.form = form()
        self.configs = AppConfigs.INSTANCE
        self.dec_sep = AppConfigs.INSTANCE['decimal.separator']
        self.min_digits = int(AppConfigs.INSTANCE['min.digits'])
        self.max_digits = int(AppConfigs.INSTANCE['max.digits'])
        self.form.setupUi(self.window)
        self.wait_operand = True
        self.wait_operand2 = True
        self.operand = 0
        self.operand2 = 0
        self.last_operand = 0
        self.memory_rec = 0
        self.display_text = ''
        self.op = CalcOperations.NO_OP
        # Find Qt components {
        self.frameMain = self.qt.find_widget(self.window, QWidget, 'frameMain')
        self.lcdDisplay = self.qt.find_widget(self.window, QLCDNumber, 'lcdDisplay')
        self.btnAC = self.qt.find_tool_button('btnAC')
        self.btnSignal = self.qt.find_tool_button('btnSignal')
        self.btnPercent = self.qt.find_tool_button('btnPercent')
        self.btnDivision = self.qt.find_tool_button('btnDivision')
        self.btn7 = self.qt.find_tool_button('btn7')
        self.btn8 = self.qt.find_tool_button('btn8')
        self.btn9 = self.qt.find_tool_button('btn9')
        self.btnMultiplication = self.qt.find_tool_button('btnMultiplication')
        self.btn4 = self.qt.find_tool_button('btn4')
        self.btn5 = self.qt.find_tool_button('btn5')
        self.btn6 = self.qt.find_tool_button('btn6')
        self.btnMinus = self.qt.find_tool_button('btnMinus')
        self.btn1 = self.qt.find_tool_button('btn1')
        self.btn2 = self.qt.find_tool_button('btn2')
        self.btn3 = self.qt.find_tool_button('btn3')
        self.btnPlus = self.qt.find_tool_button('btnPlus')
        self.btn0 = self.qt.find_tool_button('btn0')
        self.btnDecimal = self.qt.find_tool_button('btnDecimal')
        self.btnEqual = self.qt.find_tool_button('btnEqual')
        # }
        self.setup_ui()

    def setup_ui(self):
        self.btnAC.clicked.connect(self.btn_ac_clicked)
        self.btnSignal.clicked.connect(self.btn_signal_clicked)
        self.btnPercent.clicked.connect(self.btn_percent_clicked)
        self.btnDivision.clicked.connect(self.btn_division_clicked)
        self.btn7.clicked.connect(self.btn7_clicked)
        self.btn8.clicked.connect(self.btn8_clicked)
        self.btn9.clicked.connect(self.btn9_clicked)
        self.btnMultiplication.clicked.connect(self.btn_multiplication_clicked)
        self.btn4.clicked.connect(self.btn4_clicked)
        self.btn5.clicked.connect(self.btn5_clicked)
        self.btn6.clicked.connect(self.btn6_clicked)
        self.btnMinus.clicked.connect(self.btn_minus_clicked)
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.btn3.clicked.connect(self.btn3_clicked)
        self.btnPlus.clicked.connect(self.btn_plus_clicked)
        self.btn0.clicked.connect(self.btn0_clicked)
        self.btnDecimal.clicked.connect(self.btn_comma_clicked)
        self.btnDecimal.setText(self.dec_sep)
        self.btnEqual.clicked.connect(self.btn_equal_clicked)
        self.frameMain.keyPressed.connect(self.key_pressed)

    def show(self):
        self.window.show()

    def key_pressed(self, key_pressed):
        if Qt.Key_1 == key_pressed:
            self.btn1_clicked()
        elif Qt.Key_2 == key_pressed:
            self.btn2_clicked()
        elif Qt.Key_3 == key_pressed:
            self.btn3_clicked()
        elif Qt.Key_4 == key_pressed:
            self.btn4_clicked()
        elif Qt.Key_5 == key_pressed:
            self.btn5_clicked()
        elif Qt.Key_6 == key_pressed:
            self.btn6_clicked()
        elif Qt.Key_7 == key_pressed:
            self.btn7_clicked()
        elif Qt.Key_8 == key_pressed:
            self.btn8_clicked()
        elif Qt.Key_9 == key_pressed:
            self.btn9_clicked()
        elif Qt.Key_0 == key_pressed:
            self.btn0_clicked()
        elif Qt.Key_Plus == key_pressed:
            self.btn_plus_clicked()
        elif Qt.Key_Minus == key_pressed:
            self.btn_minus_clicked()
        elif Qt.Key_Slash == key_pressed:
            self.btn_division_clicked()
        elif Qt.Key_Percent == key_pressed:
            self.btn_percent_clicked()
        elif Qt.Key_Equal == key_pressed or Qt.Key_Return == key_pressed:
            self.btn_equal_clicked()
        elif Qt.Key_Backspace == key_pressed:
            self.remove_digit()
        elif Qt.Key_Period == key_pressed or Qt.Key_Comma == key_pressed:
            self.btn_signal_clicked()
        elif Qt.Key_Escape == key_pressed:
            self.btn_ac_clicked()

    def display(self, value):
        future_digits = len(str(value)) if value else 0
        digits = self.lcdDisplay.digitCount()
        if future_digits > digits:
            self.lcdDisplay.setDigitCount(min(future_digits, self.max_digits))
        elif future_digits <= digits:
            self.lcdDisplay.setDigitCount(max(future_digits, self.min_digits))
        self.lcdDisplay.display(value)

    def blink_lcd(self):
        blink = MainView.BlinkLcdThread(self.lcdDisplay)
        blink.start()
        self.display_text = ''

    def soft_reset(self):
        self.wait_operand = True
        self.wait_operand2 = True
        self.last_operand = self.operand2
        self.operand = 0
        self.operand2 = 0
        self.memory_rec = 0
        self.display_text = ''

    def append_digit(self, digit: int):
        self.btnAC.setText('C')
        if not self.display_text or self.display_text == '0':
            self.display_text = str(digit)
        else:
            self.display_text += str(digit)
        self.display(self.display_text)

    def remove_digit(self):
        if not self.display_text:
            return
        elif len(self.display_text) <= 1:
            self.btn_ac_clicked()
            return
        else:
            self.display_text = self.display_text[:-1]
        self.display(self.display_text)

    def calculate(self):
        result = 0
        if not self.op or not self.operand:
            return
        elif self.op == CalcOperations.SUM:
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
        self.display(result)
        self.memory_rec = 0

    def change_op(self, op: CalcOperations):
        self.op = op
        if self.wait_operand:
            self.operand = self.lcdDisplay.value()
            self.memory_rec = self.operand
            self.wait_operand = False
        elif self.wait_operand2:
            self.operand2 = self.lcdDisplay.value()
            self.wait_operand2 = False
        if not self.wait_operand and not self.wait_operand2:
            self.calculate()
            self.operand = self.lcdDisplay.value()
            self.wait_operand2 = True
        self.blink_lcd()

    def btn_equal_clicked(self):
        log.info("Clicked: =")
        if self.wait_operand:
            self.operand = self.lcdDisplay.value()
            self.operand2 = self.last_operand
        elif self.wait_operand2:
            self.operand2 = self.lcdDisplay.value()
        self.calculate()
        self.soft_reset()
        self.blink_lcd()

    def btn_ac_clicked(self):
        log.info("Clicked: AC")
        if self.memory_rec:
            self.memory_rec = 0
        else:
            self.lcdDisplay.setDigitCount(self.min_digits)
            self.display(0)
            self.soft_reset()
            self.btnAC.setText('AC')
        self.display_text = ''
        self.blink_lcd()

    def btn_signal_clicked(self):
        log.info("Clicked: +-")
        self.display(self.lcdDisplay.value() * -1)
        self.display_text = str(self.lcdDisplay.value())

    def btn_percent_clicked(self):
        log.info("Clicked: %")
        if not self.memory_rec:
            self.display(self.lcdDisplay.value() / 100)
        else:
            operand1 = self.memory_rec
            operand2 = self.lcdDisplay.value()
            self.display(operand1 * (operand2/100))
        self.display_text = self.lcdDisplay.value()
        self.memory_rec = self.lcdDisplay.value()

    def btn_division_clicked(self):
        log.info("Clicked: /")
        self.change_op(CalcOperations.DIVISION)

    def btn7_clicked(self):
        log.info("Clicked: 7")
        self.append_digit(7)

    def btn8_clicked(self):
        log.info("Clicked: 8")
        self.append_digit(8)

    def btn9_clicked(self):
        log.info("Clicked: 9")
        self.append_digit(9)

    def btn_multiplication_clicked(self):
        log.info("Clicked: x")
        self.change_op(CalcOperations.MULTIPLICATION)

    def btn4_clicked(self):
        log.info("Clicked: 4")
        self.append_digit(4)

    def btn5_clicked(self):
        log.info("Clicked: 5")
        self.append_digit(5)

    def btn6_clicked(self):
        log.info("Clicked: 6")
        self.append_digit(6)

    def btn_minus_clicked(self):
        log.info("Clicked: -")
        self.change_op(CalcOperations.SUBTRACTION)

    def btn1_clicked(self):
        log.info("Clicked: 1")
        self.append_digit(1)

    def btn2_clicked(self):
        log.info("Clicked: 2")
        self.append_digit(2)

    def btn3_clicked(self):
        log.info("Clicked: 3")
        self.append_digit(3)

    def btn_plus_clicked(self):
        log.info("Clicked: +")
        self.change_op(CalcOperations.SUM)

    def btn0_clicked(self):
        log.info("Clicked: 0")
        self.append_digit(0)

    def btn_comma_clicked(self):
        log.info("Clicked: ,")
        if self.dec_sep not in self.display_text:
            self.display_text += self.dec_sep if self.display_text else '0' + self.dec_sep
        self.display(self.display_text)
