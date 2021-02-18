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
puls = Button(6)
motor = Motor(26, 20)
speed = 0
def set_rpm(_rpm_soll):
   global rpm_is, speed
   rpm_soll = _rpm_soll
   step = 0.01
   #speed = 0
   error = 0
   while True:
      if error < 0:
         speed = speed  -step
      else:
         speed = speed + step
      if speed >1:
         speed = 1
      if speed < 0:
         speed = 0
      motor.forward(speed)
      #rpm_is = rpm()
      if rpm_is:
         #error = rpm_soll/rpm_is
         error = rpm_soll-rpm_is
         print(rpm_is, error)
         if error == 0:
            break
      time.sleep(0.1)

def callback_rpm():
   global old_edge, new_edge, rpm_is, edge
   edge = True
   old_edge = new_edge
   new_edge = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
   rpm_is = int(60/(((new_edge-old_edge)*10**(-9))*20))


def callback_puls_low():
   pass
def rpm():
   global old_edge, new_edge
   if old_edge and new_edge:
      return int(60/(((new_edge-old_edge)*10**(-9))*20))

puls.when_pressed = callback_rpm
#puls.is_released = callback_puls_low

while True:
   n = int(input('rpm: '))
   set_rpm(n)

