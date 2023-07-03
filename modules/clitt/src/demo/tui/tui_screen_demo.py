#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib
   @package: demo.cli.tui
      @file: tui_screen_demo.py
   @created: Fri, 23 Jun 2023
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from clitt.core.tui.tui_screen import TUIScreen
from hspylib.modules.cli.vt100.vt_utils import get_cursor_position
from time import sleep


def draw(scr: TUIScreen):
    scr.cursor.erase(TUIScreen.ScreenPortion.SCREEN)
    scr.cursor.home()
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.move_to(3, 20)
    scr.cursor.write("X")


def resized():
    print("Resized")


if __name__ == "__main__":
    screen = TUIScreen(False, False, resized)
    draw(screen)
    sleep(1)
    screen.cursor.erase(TUIScreen.CursorDirection.UP)
    sleep(1)
    draw(screen)
    sleep(1)
    screen.cursor.erase(TUIScreen.CursorDirection.DOWN)
    sleep(1)
    draw(screen)
    screen.cursor.erase(TUIScreen.CursorDirection.LEFT)
    sleep(1)
    draw(screen)
    screen.cursor.erase(TUIScreen.CursorDirection.RIGHT)
    sleep(1)
    draw(screen)
    screen.cursor.erase(TUIScreen.ScreenPortion.LINE)
    sleep(1)
    draw(screen)
    screen.cursor.move_to(screen.cursor.bottom[0], screen.cursor.bottom[1])
    sleep(1)
    screen.cursor.write("123")
    screen.cursor.move_to(3, 3)
    sleep(1)
    screen.cursor.write("@")
    sleep(1)
    screen.cursor.move(5, TUIScreen.CursorDirection.RIGHT)
    screen.cursor.write("#")
    sleep(1)
    screen.cursor.move(2, TUIScreen.CursorDirection.DOWN)
    screen.cursor.write("#")
    sleep(1)
    screen.cursor.move(5, TUIScreen.CursorDirection.LEFT)
    screen.cursor.write("#")
    sleep(1)
    screen.cursor.move(2, TUIScreen.CursorDirection.UP)
    screen.cursor.write("#")
    sleep(1)
    screen.cursor.end()
    print(get_cursor_position(), screen.cursor)
