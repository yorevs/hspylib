from threading import Thread
from time import sleep

from PyQt5.QtWidgets import QLCDNumber

from hspylib.core.config.app_config import AppConfigs


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
