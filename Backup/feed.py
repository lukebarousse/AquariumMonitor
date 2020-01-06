#!/usr/bin/env python

# Let's import the GPIO library to control the pins
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
FEED_SERVO_CONTROL_PIN = 18

try:
  # Here we are configuring our PIN to OUPUT to send current through it
  GPIO.setup(FEED_SERVO_CONTROL_PIN, GPIO.OUT)
  # Now we have to set the pulse wave modulations
  '''
  FROM ADAFRUIT DOCUMENTATION, the controls of the servo are :  
  FULL SPEED FORWARD --> Position "180" requires 2ms pulse 
  FULL SPEED BACKWARD -->  Position "0" requires 1ms pulse 
  STOP --> Position "90" requires 1.5ms pulses
  PWM is a way to send some pulses to the control PIN of the servo.
  For example, a PWM at 1 Hertz means 1 pulse every second.
  Let's take 100 Hertz as an example.
  '''

  PWM_FREQUENCY = 100 # In Hertz, which means 100 pulses in 1secs (1000ms) --> 1 pulse = 10ms

  '''
  However, 20ms pulses are still too long for FORWARD (2ms) or BACKWARD(1ms).
  Looking at the documentation of PWM we can also set duty cycle.
  We use the following calculation : DCPurcentage = ( ms_required / PWM_FRQ ) x 100 (to have a % between 0 and 100)
  for FORWARD : ( 2 / 10 ) X 100 = 20% of dutycycle.
  for BACKWARD : ( 1 / 10 ) X 100 = 10% of dutycycle.
  '''

  FULL_SPEED_FORWARD_DC = 20
  FULL_SPEED_BACKWARD_DC = 10
  pwm = GPIO.PWM(FEED_SERVO_CONTROL_PIN, PWM_FREQUENCY)

  # Start the SERVO moving forward
  pwm.start(FULL_SPEED_FORWARD_DC)

  # we only activate 0.5 seconds forward
  # Not to much food for the pet !
  time.sleep(0.5)

  # (OPTINAL) If we want to go back to initial position
  # This is to demonstrate the backward feature
  pwm.ChangeDutyCycle(FULL_SPEED_BACKWARD_DC)
  time.sleep(0.5)

  # Clean everything
  pwm.stop()
  time.sleep(0.5)
  GPIO.cleanup()

  result = True
except:
  result = False

# Return result
print "Feeding completed" if result else "Something went wrong"