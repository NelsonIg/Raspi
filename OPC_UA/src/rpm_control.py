#!/usr/bin/env python3

import sys
import time
from gpiozero import Motor, Button
import time

edge = False
old_edge = False
new_edge = False
rpm_is = False
downtime = None
#puls = Button(14)
motor = Motor(26, 20)
speed = 0
callback_flag, callback_count = False, 0

def set_rpm(_rpm_soll):
   global rpm_is, speed
   # initial values
   rpm_soll = _rpm_soll
   step = 0.01
   error = 0
   # Ajust speed according to error
   while True:
      if error < 0:
         # Too slow
         speed = speed  - step
      else:
         # Too fast
         speed = speed + step
      # speed must be in range 0-1
      if speed >1:
         speed = 1
      if speed < 0:
         speed = 0
      motor.forward(speed)
      # Start Controlling speed if RPM is available
      rpm_is = rpm()
      if rpm_is >-1:
         error = rpm_soll-rpm_is
#         print(rpm_is, error)
         if error == 0:
            # Stop controlling
            break
      time.sleep(0.1)



def hold_rpm(_rpm_soll):
   global rpm_is, speed
   # initial values
   rpm_soll = _rpm_soll
   step = 0.002
   sample_time = 0.05 # sec
   error = 0
   # Ajust speed according to error
   while True:
      if error < 0:
         # Too slow
         speed = speed  - step
      else:
         # Too fast
         speed = speed + step
      # speed must be in range 0-1
      if speed >1:
         speed = 1
      if speed < 0:
         speed = 0
      motor.forward(speed)
      # Start Controlling speed if RPM is available
      rpm_is = rpm()
      if rpm_is >-1:
         error = rpm_soll-rpm_is
#         print(rpm_is, error)
      time.sleep(sample_time)

def callback_rpm():
   global old_edge, new_edge, rpm_is, edge, callback_flag
   edge = True
   old_edge = new_edge
   new_edge = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
   callback_flag = True
   # rpm_is = int(60/(((new_edge-old_edge)*10**(-9))*20))


def callback_puls_low():
   pass

def rpm():
   global old_edge, new_edge, callback_flag, callback_count, rpm_is
   if callback_flag:
      callback_flag , callback_count = False, 0
      if old_edge and new_edge:
         return int(60/(((new_edge-old_edge)*10**(-9))*20))
      else:
         return -1
   else:
      if callback_count >10:
         return 0
      return -1

if __name__ == '__main__':

   #puls.when_pressed = callback_rpm
#puls.is_released = callback_puls_low

   #while True:
      #n = int(input('rpm: \n-1: stopp\n'))
      #if n < 0: break
      #set_rpm(n)
#     hold_rpm(100)
   motor.forward(0.5)
   while True:
      time.sleep(10)
