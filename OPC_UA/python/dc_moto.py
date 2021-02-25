#!/usr/bin/env python3

import sys
import time
from gpiozero import Motor, Button
import time

pulses = 0
old_edge = False
new_edge = False

def callback_rpm():
   global old_edge, new_edge, pulses
   old_edge = new_edge
   new_edge = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
def rpm():
   global old_edge, new_edge
   if old_edge and new_edge:
      return 60/(((new_edge-old_edge)*10**(-9))*20)

def main():
   motor = Motor(26, 20)
   button = Button(6)
   button.when_pressed = callback_rpm

   for _ in range(3):
      speed = float(input('speed: '))
      motor.forward(speed)
      for _ in range(61):
         print(rpm())
         time.sleep(1)
   motor.stop()


if __name__=='__main__':
   main()
