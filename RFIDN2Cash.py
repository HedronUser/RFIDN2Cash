#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 12:02:22 2017

@author: root
"""
import time
import curses
#import RPi.GPIO as GPIO #only works on Raspberry Pi

#GPIO.setmode(GPIO.BCM) #sets how the pins are labeled on the RPi
#GPIO.setup(23,GPIO.OUT) #sets up pin 23 as an output
#GPIO.set(23, GPIO.LOW) #initializes the pin to LOW. Laser off.

#dictionary stores RFID as keys and purchased tool time as values (minutes)
credit_dict = { '0007421597': 0, '1512305969': 0,  '0007394263': 60, '0007406707': 0, '0007411862': 0, '0007395322': 0, '0007410979': 0, '0007416591':0.1, '0007398453':0}

def Get_RFID():
    #returns RFID as a string
    #takes in nothing
    
    #initialize a list to store keyboard input
    rfidread = []
    
    #iterates over read character and add characters to list
    for i in range(11):
        c = stdscr.getch() #captures keystrokes
        chrc = chr(c) #converts the keystrokes which comes in as ASCII values (0-255)
        if chrc == '\n': #ends list at a newline
            break    
        else:rfidread.append(chrc)
            
    #initialize empty string
    readtag = ""

    #convert list to string
    for j in range(10):
        readtag += rfidread[j]
    
    return readtag

def User_authorized(readtag):
    #if user is authorized function returns 1
    #if user is not authorized (RFID TAG NOT IN DICTIONARY) returns 0
    
    if readtag in credit_dict.keys():
        print("User Authorized")
        time.sleep(2)
        return 1
    else:
        print("Unauthorized User")
        time.sleep(2)
        return 0
        #break
        
def Toggle_tool(state):
    #enables tool and returns 1 if state is 0
    #disables tool and returns 0 if state is 1
    if state == 0:
        print("enable tool")
        #enable tool command
        #GPIO.set(23, GPIO.HIGH) 
        state = 1
        return state
    elif state == 1:
        print("disable tool")
        #disable tool command
        #GPIO.set(23, GPIO.LOW)
        state = 0
        return state
    else:
        return print("State Not recognized")

try:
    stdscr = curses.initscr() 
    curses.noecho()
    curses.nocbreak()
    #stdscr.keypad(1)
    #initialize state variable
    state = 0
    #d = stdscr.getch()
    while 1:
        #get a reading from reader 
        Current_readtag = Get_RFID()
        if User_authorized(Current_readtag) == 1:
            #print to LCD
            print("User authorized")
            #enable the tool
            Toggle_tool(0)
        elif User_authorized(Current_readtag) == 0:
            print("User unauthorized")
        
        

        
finally:
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()