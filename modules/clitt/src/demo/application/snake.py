#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time


def snake():
    # initialize the curses library
    stdscr = curses.initscr()

    # turn off line buffering
    curses.cbreak()

    # hide the cursor
    curses.curs_set(0)

    # use color if possible
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # set up the screen dimensions
    rows, cols = stdscr.getmaxyx()

    # create the game window
    win = curses.newwin(rows - 2, cols - 2, 1, 1)

    # turn on keypad input
    win.keypad(1)

    # set up the snake
    snake = [(rows // 2, cols // 2)]

    # set up the food
    food = (rows // 2, cols // 2 + 1)

    # main loop
    while True:
        # clear the screen
        win.clear()

        # draw the snake
        for row, col in snake:
            win.addstr(row, col, '#', curses.color_pair(1))

        # draw the food
        win.addstr(food[0], food[1], '$', curses.color_pair(1))

        # refresh the screen
        win.refresh()

        # get the next key
        key = win.getch()

        # handle the key
        if key == curses.KEY_UP:
            snake.insert(0, (snake[0][0] - 1, snake[0][1]))
        elif key == curses.KEY_DOWN:
            snake.insert(0, (snake[0][0] + 1, snake[0][1]))
        elif key == curses.KEY_LEFT:
            snake.insert(0, (snake[0][0], snake[0][1] - 1))
        elif key == curses.KEY_RIGHT:
            snake.insert(0, (snake[0][0], snake[0][1] + 1))

        # remove the tail of the snake
        snake.pop()

        # check for food
        if snake[0] == food:
            food = (snake[0][0], snake[0][1] + 1)
            snake.insert(0, (snake[0][0], snake[0][1] + 1))

        # sleep for a short time
        time.sleep(0.1)

    # turn off keypad input
    win.keypad(0)

    # show the cursor
    curses.curs_set(1)

    # turn on line buffering
    curses.nocbreak()

    # end the curses library
    curses.endwin()


if __name__ == '__main__':
    snake()
