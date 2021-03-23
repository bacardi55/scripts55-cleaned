#!/usr/bin/env python3

# Author: Raphael <bacardi55> Khaiat
# Date: 2019/08/27

# TODO:
# - Manage motion start/stop via systemctl
# - URL setup at top of the script for easier config
# - file path setup at top of the script for easier config

# Dependencies:
# - paho-mqtt
# - requests

import paho.mqtt.client as mqtt
import requests
import time
import subprocess

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("home/entry/#")

# Take a new snapshot.
def take_snapshot():
    manage_motion("true")
    # Let motion adapt to light
    time.sleep(10)
    # motion API available only locally.
    r = requests.get('http://127.0.0.1:5555/0/action/snapshot')
    time.sleep(1)
    manage_motion("false")

# Send snapshot to nodered.
def send_snapshot():
    print("In send snap")
    files = {'upload_file': open('/var/motion/pictures/lastsnap.jpg','rb')}
    r2 = requests.post("http://<NoderedIP>:<NoderedPort>/api/home/entry/camera/snapshot", files=files)

def manage_motion(option=True):
    print("Manage motion: %s" % option)
    if option == "true":
        subprocess.Popen("sudo systemctl start motion.service", shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        subprocess.Popen("sudo systemctl stop motion.service", shell=True, stdout=subprocess.PIPE).stdout.read()


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    if msg.topic == "home/entry/snapshot":
        take_snapshot()
        time.sleep(1)
        send_snapshot()

    elif msg.topic == "home/entry/camera":
        # if value is true, start motion.
        # else, stop motion.
        manage_motion(msg.payload.decode('UTF-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("<MosquittoIP>", 5883, 60)

client.loop_forever()
