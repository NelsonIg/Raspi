#!/usr/bin/env python3

import asyncio
import logging
from datetime import datetime
import time
from asyncua import ua, uamethod, Server


# Class for Subscription Handling
class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)

async def motor_object(idx):
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
    base_motor = await motor_object(idx)


    # populateing address space
    motor = await server.nodes.objects.add_object(idx, "Motor", base_motor)
    rpm_var = await motor.get_child([f"{idx}:RPM"]) # rounds per minute
    await rpm_var.set_writable()
    speed_var = await motor.get_child([f"{idx}:Speed"]) # motor speed
    await speed_var.set_writable()
    
    # Start!
    async with server:
        while True:
            await asyncio.sleep(0.1)
            

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    