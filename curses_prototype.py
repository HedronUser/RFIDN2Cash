#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:39:01 2017

@author: root
"""

import curses, traceback

def main(stdscr):
    #program returns 0 if there is an error
    #program returns keyboard input if no errors
    c = stdscr.getch()
    #print(c)
    if c!= curses.ERR:
        return 0
    else:
        return c

def cleanup():
    #program cleans up curses terminal
    #curses.initscr()
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    
while True:
    try:
        stdscr = curses.initscr()
        stdscr.refresh()
        curses.noecho()
        curses.cbreak()
        if main(stdscr) != -1 :
            #sleep(1)
            print(main(stdscr))
        cleanup()
    except NameError:
        print("no input")
        