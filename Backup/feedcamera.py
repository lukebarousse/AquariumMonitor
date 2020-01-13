#!/usr/bin/env python

import RPi.GPIO as GPIO
# time library to delay a bit some commands
import time
# os library for us to run command lines in Python
# we need this to enable/disable our camera server
import os

# Let's set our GPIO BCM numbers into variables for code clarity
# INPUT is the pin receiving the button state "on" = False, "off" = True
CAMERA_BTN_INPUT = 9
FEED_BTN_INPUT = 25
# OUTPUT is going to enable disable the led button
# GPIOs are capable of sending 3V through their pin !
CAMERA_BTN_LED_OUTPUT = 23
FEED_BTN_LED_OUTPUT = 22

try:
    # Set the mode to BCM to work according to BCM number and not physical slots.
    GPIO.setmode(GPIO.BCM)

    # Set INPUT to analyse incoming signal
    GPIO.setup(CAMERA_BTN_INPUT, GPIO.IN)
    GPIO.setup(FEED_BTN_INPUT, GPIO.IN)
    # Set OUPUT as a conditional 3V power pin
    GPIO.setup(CAMERA_BTN_LED_OUTPUT, GPIO.OUT)
    GPIO.setup(FEED_BTN_LED_OUTPUT, GPIO.OUT)

    while True:
        # Handle the CAMERA toggle
        if GPIO.input(CAMERA_BTN_INPUT) == False:
            print("CAMERA Pressed")
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.HIGH)
            time.sleep(0.1)
            # Remember this command from tutorial 1 ? so usefull right ?
            # It allows us to quickly start the camera server
            command = 'sudo service motion start'
            p = os.system(command)
        else:
            print("CAMERA Off")
            GPIO.output(CAMERA_BTN_LED_OUTPUT, GPIO.LOW)
            time.sleep(0.1)
            command = 'sudo service motion stop'
            p = os.system(command)

        # Handle the FEED toggle
        if GPIO.input(FEED_BTN_INPUT) == False:
            print("FEED Pressed")
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.HIGH)
            time.sleep(0.1)
            command = 'python /var/www/html/pet-preset1_1/feed.py'
            p = os.system(command)
        else:
            print("FEED Off")
            GPIO.output(FEED_BTN_LED_OUTPUT, GPIO.LOW)

except KeyboardInterrupt:
    print
    'interrupted!'
    GPIO.cleanup()

# Clean everything
GPIO.cleanup()