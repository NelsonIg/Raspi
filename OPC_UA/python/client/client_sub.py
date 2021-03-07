#!/usr/bin/env python3

import asyncio
import logging
import time
from sys import argv

from asyncua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

# measure time of PublishResult intervals
last_pub_result = 0 # ns
new_pub_result = 0 # ns

class SubscriptionHandler:
    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """

    # measure time of PublishResult intervals
    last_pub_result = 0  # ns
    new_pub_result = 0  # ns
    timestamps = [] # store elapsed_time continuously here
    def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """
        self.last_pub_result = self.new_pub_result
        self.new_pub_result = time.perf_counter_ns()
        elapsed_time = self.new_pub_result-self.last_pub_result
        self.timestamps.append(elapsed_time)
        _logger.info(f'datachange_notification {node} {val} {elapsed_time}')

async def main(host_ip='192.168.0.183'):
    # client with server url and 4 sec. timout
    client = Client(url=f'opc.tcp://{host_ip}:4840/freeopcua/server/', timeout=4)
    not_connected = True
    while not_connected:
        try:
            async with client:
                not_connected = False
                idx = await client.get_namespace_index(uri="example-uri.edu")
                # get Motor Node
                rpm_var = await client.nodes.objects.get_child([f"{idx}:Motor", f"{idx}:RPM"])
                speed_var = await client.nodes.objects.get_child([f"{idx}:Motor", f"{idx}:Speed"])
                # create subscription
                handler = SubscriptionHandler()
                subscription = await client.create_subscription(period=50, handler=handler) # 100ms publishing interval
                # Subscribe to data change
                await subscription.subscribe_data_change(nodes=rpm_var, queuesize=1)
                # Set Speed
                await speed_var.write_value(0.2)
                # Run subscription forever
                while True:
                    await asyncio.sleep(1)
                    # check if connection still alive
                    try:
                        await rpm_var.read_value()
                    except ConnectionError as e:
                        # Connection is closed
                        _logger.info(e)
                        # leave context manager to close connection
                        break
        except Exception as e:
            _logger.info(e)
    print(handler.timestamps)


if __name__ == '__main__':
    if len(argv)>1:
        _logger.info(f'Host_ip:\t\t{argv[1]}')
        # arguments entered
        asyncio.run(main(argv[1]))
    else:
        asyncio.run(main())