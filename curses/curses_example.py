#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:37:35 2017

@author: root
"""

import curses
damn = curses.initscr()
damn.nodelay(1) # doesn't keep waiting for a key press
damn.keypad(1) # i.e. arrow keys
curses.noecho() # stop keys echoing
c = 0
damn.addstr(0, 0, "q to quit - only the up and down arrow keys do anything")
while c != ord('q'):
  c = damn.getch()
  if c == curses.KEY_UP:
    damn.addstr(1, 0, "up key pressed \n")
  if c == curses.KEY_DOWN:
    damn.addstr(1, 0, "\n down key pressed")
    
curses.endwin()