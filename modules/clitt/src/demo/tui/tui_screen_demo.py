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
from clitt.core.term.commons import Direction, get_cursor_position, Portion
from clitt.core.term.screen import Screen
from time import sleep


def draw(scr: Screen):
    scr.cursor.erase(Portion.SCREEN)
    scr.cursor.home()
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.writeln("." * 40)
    scr.cursor.move_to(3, 20)
    scr.cursor.write("X")


if __name__ == "__main__":
    screen = Screen()
    draw(screen)
    sleep(0.5)
    screen.cursor.erase(Direction.UP)
    sleep(0.5)
    draw(screen)
    sleep(0.5)
    screen.cursor.erase(Direction.DOWN)
    sleep(0.5)
    draw(screen)
    screen.cursor.erase(Direction.LEFT)
    sleep(0.5)
    draw(screen)
    screen.cursor.erase(Direction.RIGHT)
    sleep(0.5)
    draw(screen)
    screen.cursor.erase(Portion.LINE)
    sleep(0.5)
    draw(screen)
    screen.cursor.move_to(screen.cursor.bottom[0], screen.cursor.bottom[1])
    sleep(0.5)
    screen.cursor.write("123")
    screen.cursor.move_to(3, 3)
    sleep(0.5)
    screen.cursor.write("@")
    sleep(0.5)
    screen.cursor.move(5, Direction.RIGHT)
    screen.cursor.write("#")
    sleep(0.5)
    screen.cursor.move(2, Direction.DOWN)
    screen.cursor.write("#")
    sleep(0.5)
    screen.cursor.move(5, Direction.LEFT)
    screen.cursor.write("#")
    sleep(0.5)
    screen.cursor.move(2, Direction.UP)
    screen.cursor.write("#")
    sleep(0.5)
    screen.cursor.end()
    print(get_cursor_position(), screen.cursor)
