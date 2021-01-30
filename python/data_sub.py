#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json, os, sys
import datetime as date
import pandas as pd

# dataframe to store sensor data
data_df = pd.DataFrame({"date": [],
                        "temperature": [],
                        "humidity": []})


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("bme280")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global data_df
    print(msg.topic+" "+msg.payload.decode())
    data = json.loads(msg.payload)  # json to dict
    now = date.datetime.now()  # get timestamp
    # append date to data
    data.update({'date': str(now)})
    # print(data)
    data_to_csv('sensor_data', data)


def data_to_csv(filename: str, data: dict):
    """store data to filename as csv"""
    now = date.datetime.now()
    file_date = f'{now.year}-{now.day}'  # one file per day
    filename = file_date+'-'+filename+'.csv'
    data_line = f"{data['date']}, {data['temperature']}, {data['humidity']}\n"  # sensor data
    if not os.path.exists(filename):
        first_line = "date,temperature,humidity\n"  # header
        print('store data to '+filename)
        with open(filename, 'w') as f:
            f.write(first_line+data_line)
    else:
        with open(filename, 'a') as f:
            f.write(data_line)



def main(mqtt_host="localhost", port=1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_host, port, 60) # connect(host, port=1883, keepalive=60 (in sec), bind_address="")
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(mqtt_host=sys.argv[1], port=int(sys.argv[2]))
    else:
        main("192.168.0.183")

