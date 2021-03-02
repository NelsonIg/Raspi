#!/usr/bin/env python3

import asyncio
import logging

from datetime import datetime

import time

from gpiozero import Motor, Button

from asyncua import ua, uamethod, Server

import threading

old_edge = False
new_edge = False
rpm_is = -1
downtime = None
puls = Button(14)
motor = Motor(26, 20)
speed = 0.0
callback_flag, callback_count = False, 0

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

def callback_rpm():
   global old_edge, new_edge, callback_flag
   old_edge = new_edge
   new_edge = time.perf_counter_ns()
   callback_flag = True

async def rpm():
   global old_edge, new_edge, callback_flag, callback_count
   _logger.info(f'\t\tCallbackCount: {callback_count}')
   if callback_flag:
      callback_flag , callback_count = False, 0
      if old_edge and new_edge:
         return  int(60/(((new_edge-old_edge)*10**(-9))*20))
      else:
         return -1
   else:
      if callback_count >10:
         return 0
      else:
         callback_count+=1
         return -1
         


# functions for updating data and controlling motor
async def set_speed(motor_var):
    '''
    Set motor speed (0.0-1.0)
    '''
    speed = await motor_var.read_value()
    try:
        motor.forward(speed)
    except ValueError:
        _logger.warning(f'\t\t{speed} no valid speed')
    return speed

async def set_speed_loop(motor_var):
    '''
    Run set_speed in loop
    '''
    while True:
        await set_speed(motor_var)
        await asyncio.sleep(0.001)
        

async def get_rpm(rpm_var):
    '''
    read round per minute periodically
    '''
    #await asyncio.sleep(0.02)
    rpm_is = await rpm()
    if rpm_is>-1:
        await rpm_var.write_value(rpm_is)
    return rpm_is


# Class for Subscription Handling
class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)
        
async def motor_object(idx, server):
    '''
    Create custom motor base object
    - BaseMotor
        - RPM
        - Speed
    '''
    # create Motor-node type for later use
    base_motor = await server.nodes.base_object_type.add_object_type(idx, "BaseMotor")
    base_rpm_var = await base_motor.add_variable(idx, "RPM", 0.0)
    await base_rpm_var.set_modelling_rule(True)
    base_speed_var = await base_motor.add_variable(idx, "Speed", 0.0)
    await base_speed_var.set_modelling_rule(True)
    return base_motor
    
    
async def main():
    global rpm_is
    
    puls.when_pressed = callback_rpm # set callback
    
    # initialize Server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://pi.local:4840/freeopcua/server/')
    server.set_server_name("OPC UA Raspi Server")
    # all possible endpoint policies set for client connection
    server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])
    
    # setup namespace
    uri = "example-uri.edu"
    idx = await server.register_namespace(uri)
    
    # create Motor-node type for later use
    base_motor = await motor_object(idx, server)


    # populateing address space
    motor = await server.nodes.objects.add_object(idx, "Motor", base_motor)
    rpm_var = await motor.get_child([f"{idx}:RPM"]) # rounds per minute
    await rpm_var.set_writable()
    speed_var = await motor.get_child([f"{idx}:Speed"]) # motor speed
    await speed_var.set_writable()
    
    # Start!
    async with server:
        # start daemon that sets motor speed
        speed_daemon = threading.Thread(target=set_speed_loop, args=[speed_var], daemon=True)
        speed_daemon.start()
        while True:
            #rpm_is, speed_is = await asyncio.gather(*(get_rpm(rpm_var), set_speed(speed_var)))
            #_logger.info(f'\t\tRPM: {rpm_is}\n\t\t\tMotor: {speed_is}')
            await get_rpm(rpm_var)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    