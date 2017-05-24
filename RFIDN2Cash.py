#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 12:02:22 2017

@author: root
"""
import sys
import time
import curses
#import logging
#
#logging.basicConfig(
#        level=logging.INFO,
#        # stream=sys.stdout,
#        filename='~/RFID2Cash/log.log',
#        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger(__name__)

import RPi.GPIO as GPIO #only works on Raspberry Pi

GPIO.setmode(GPIO.BCM) #sets how the pins are labeled on the RPi
GPIO.setup(23,GPIO.OUT) #sets up pin 23 as an output
GPIO.output(23, 0) #initializes the pin to LOW. Laser off.


def get_RFID():
    
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

def user_authorized(readtag):
    #if user is authorized function returns 1
    #if user is not authorized (RFID TAG NOT IN DICTIONARY) returns 0
    
    if readtag in Credit_dict.keys():
#        logger.debug("User Authorized")
        #time.sleep(2)
        return 1
    else:
#        logger.debug("Unauthorized User")
        #time.sleep(2)
        return 0
        #break
        
#class Tool(object):
#    def __init__(self, state=False):
#        self.state = state
#    
#    def toggle(self):
#        self.state = not self.state
#
#TOOL = Tool()

def toggle_tool(state):
# def toggle_tool(): should be lowercase
#     TOOL.toggle()
# state is a singleton (one in memory)
# this should be something like tool.toggle() where tool.state is 0 or 1
    
    #enables tool and returns 1 if state is 0
    #disables tool and returns 0 if state is 1
    if state == 1:
        print("enable tool")
        #enable tool command
        GPIO.output(23, 1) 
        state = 1
        return state
    elif state == 0:
        print("disable tool")
        #disable tool command
        GPIO.output(23, 0)
        state = 0
        return state
    else:
        return print("State Not recognized")

def user_credit(readtag):
    #returns 0 if user is out of credit 
    #returns 1 if user has credit
    #takes in as an argument the RFID tag #

    if Credit_dict[readtag] == 0:
        return 0
    elif Credit_dict[readtag] > 0:
        return 1

#def Display_user_credit(readtag):
    #displays the user credit left on LCD screen
    #takes in as an argument the RFID tag #
    #insert code for LCD screen write, variable to use is credit_dict[readtag]

def user_login(readtag):
    #returns 1 if the user is logged in already
    #returns 0 if the user is not logged in
    #takes as an argument the RFID of the user.
    if user_logged_in == 0:
        return 0
    else:
        return 1

def time_tracker(usertime):
    #returns the time user has been using the machine.
    #if argument is 1, timer starts and function returns start time in seconds
    #if argument is 0, timer ends and elapsed time is returned in minutes 
    
    if usertime == 1:
        global start
        start = time.time() #time at beginning 
        return start
    if usertime == 0:
        end = time.time() #at some other point
        elapsed = (end - start) / 60
        return elapsed

def user_update(ID, usage):
    #takes as an argument the time in minutes that the user used the laser
    #returns nothing if successful
    #returns 0 if user ran out of credit.
    #updates a dictionary 
    global Credit_dict
    #store old user credit value
    Current_credit = Credit_dict[ID] 
    Credit_dict[ID] = Current_credit - usage
    if Credit_dict[ID] <= 0:
        return 0
           
#initialize global state variable to store machine state
state = 0

#initialize global variable to store time
usage = 0

#add dictionary that stores RFID as keys and corresponding purchased tool time as values (minutes)
Credit_dict = { '0007421597': 0, '1512305969': 0,  '0007394263': 60, '0007406707': 0, '0007411862': 0, '0007395322': 0, '0007410979': 0, '0007416591':0.1, '0007398453':0}

#initialize global variable to store user
user_logged_in = 0

try:
    #initialize curses window functions
    stdscr = curses.initscr() 
    curses.noecho()
    curses.nocbreak()
   
    #start main loop
    while 1:
        #need something to prevent other users from interrupting
        #need something to cancel machine
        
        #get and store a reading from reader 
        Current_readtag = get_RFID()
        
        
        #conditional should check if RFID is in dictionary                            
        if user_authorized(Current_readtag) == 1:
            #print to LCD
            #print("User authorized") #print statement would be unnecessarily repeated

            #if user is already logged in, store login time, update dict, turn off tool, log user out
            if user_login(Current_readtag) == 1:
                
                #turn off tool
                toggle_tool(0)
                
                #store elapsed time used tool and update dictionary
                usage = time_tracker(0)
                status = user_update(Current_readtag, usage)
                
                if status == 0:
                    print("User ran out of time")
                    #print to LCD
                
                #log person out by updating user variable
                user_logged_in = 0
            
            #executes if user is not already logged in    
            elif user_login(Current_readtag) == 0:    #add "and user is not different from last logged in user" to this statement?
                #return and store bool if user has credit or not
                Credit_status = user_credit(Current_readtag)
            
                #store user credit as variable
                Credit_remaining = Credit_dict[Current_readtag]
            
                if Credit_status == 0:
                    #print to LCD
                    #eventually use real username from django class
                    print("User Out of Credit, Please Refill")
                    #disable tool
                    toggle_tool(0)
                    
                elif Credit_status == 1:
                    #print to LCD
                    print("Tool enabled, User Credit Remaining: "+ str(Credit_remaining))
                    
                    #update login variable
                    user_logged_in = 1
                   
                    #turn machine on
                    toggle_tool(1)
                    
                    #start tracking user time in seconds
                    time_tracker(1)
                        
                    #tell user they are low on credit
                    if Credit_remaining < 5:
                            print("User credit is 5 minutes or less")
                            
                
            
        else:
            print("Scan your RFID")
        #clear RFID for next scan event
        Current_readtag = 0
        
        
        
finally:
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()
