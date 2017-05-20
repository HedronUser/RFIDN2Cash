#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 12:02:22 2017

@author: root
"""

import curses

tag = '0007416591'

try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.nocbreak()
    #stdscr.keypad(1)
    #initialize the tool off
    scanmode = 0
    #GPIO.set(23, GPIO.LOW)
    
    while 1:
        #c = stdscr.getch()
        rfidread = []
        
        #iterate over tag and convert to characters in a list
        for i in range(11):
            c = stdscr.getch()
            chrc = chr(c)
            if chrc == '\n':
                break    
            else:rfidread.append(chrc)
            
        print(rfidread)
        
        #initialize empty string
        readtag = ""
        #print(len(rfidread))
        #convert list to string
        for j in range(10):
            readtag += rfidread[j]
        
        print(readtag)
        
        
        if scanmode == 0:
            print("enable tool")
            #enable tool command
            #GPIO.set(23, GPIO.HIGH)
            scanmode = 1
        elif scanmode == 1:
            print("disable tool")
            #disable tool command
            #GPIO.set(23, GPIO.LOW)
            scanmode = 0
        
        #convert the list to a string
                
        #if int(tag1) == c:
        #    stdscr.addstr("recognized addstr")
        #print(c)
        if c == ord('q'): break
finally:
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()