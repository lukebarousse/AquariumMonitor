#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#possible that have more than one script on the GPIO circiut it will throw a warning.  lets disable the warnings.
#GPIO.setwarnings(False)

# this specifies the mode you are using, BCM refers to numbering style we will be using.
GPIO.setmode(GPIO.BCM)

# initialize list with pin numbers
channel = [17]

# set channel as an output, can use list or tuples for pinlist
GPIO.setup(channel, GPIO.OUT)

# Set the output of the channel
# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.output(channel, GPIO.LOW)
print("Feeding Fish")
time.sleep(0.5)
GPIO.output(channel, GPIO.HIGH)
print("Fish Fed")

# Reset GPIO settings
GPIO.cleanup()