import paho.mqtt.client as mqtt
import json
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
    # construct dataframe
    df = pd.DataFrame({"date": [str(now)],
                       "temperature": [data['temperature']],
                       "humidity": [data['humidity']]})
    data_df = data_df.append(df, ignore_index=True)  # append to global DataFrame
    print(data_df)
    data_df.to_csv("sensorData.csv")


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
    main("192.168.0.183")

