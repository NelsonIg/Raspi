#!/usr/bin/env python3

import sys
import time
from gpiozero import Motor, Button
import time

import logging

import asyncio
import sys
sys.path.insert(0, "..")



from asyncua import ua, Server
from asyncua.common.methods import uamethod

edge = False
old_edge = False
new_edge = False
rpm_is = -1
downtime = None
puls = Button(14)
speed = 0
callback_flag, callback_count = False, 0

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

def callback_rpm():
   global old_edge, new_edge, rpm_is, edge, callback_flag
   edge = True
   old_edge = new_edge
   new_edge = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
   callback_flag = True

async def rpm():
   global old_edge, new_edge, callback_flag, callback_count, rpm_is
   _logger.info(f'CallbackCount: {callback_count}')
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
         
   
      
@uamethod
def func(parent, value):
    return value * 2


async def main():
    global rpm_is
    puls.when_pressed = callback_rpm # set callback
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://pi.local:4840/freeopcua/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, 'Car')
    rpm_var = await myobj.add_variable(idx, 'rpm', 0)
    motor_var = await myobj.add_variable(idx, 'motor', 0)
    # Set MyVariable to be writable by clients
    await rpm_var.set_writable()
    await motor_var.set_writable()
    await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)
            rpm_is = await rpm()
            if rpm_is>-1:
                await rpm_var.write_value(rpm_is)
                _logger.info(f'\nRPM: {rpm_is} Motor: {await motor_var.read_value()}')
            


if __name__ == '__main__':
    asyncio.run(main())