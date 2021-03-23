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
    client.subscribe("home/livingRoom/piscreen/#")


def manage_screen(option=True):
    print("Manage screen: %s" % option)
    if option == "true":
        subprocess.Popen("sudo rpi-backlight --on", shell=True, stdout=subprocess.PIPE).stdout.read()
    else:
        subprocess.Popen("sudo rpi-backlight --off", shell=True, stdout=subprocess.PIPE).stdout.read()


def manage_power(option=True):
    print("Manage Power: %s" % option)
    if option == "true":
        subprocess.Popen("sudo shutdown -h now", shell=True, stdout=subprocess.PIPE).stdout.read()


def manage_reboot(option=True):
    print("Manage Reboot: %s" % option)
    if option == "true":
        subprocess.Popen("sudo shutdown -r now", shell=True, stdout=subprocess.PIPE).stdout.read()


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))

    if msg.topic == "home/livingRoom/piscreen/screen":
        # if value is true, start screen
        # else, stop screen.
        manage_screen(msg.payload.decode('UTF-8'))

    elif msg.topic == "home/livingRoom/piscreen/reboot":
        # if value is true, shutdown Pi.
        manage_reboot(msg.payload.decode('UTF-8'))

    elif msg.topic == "home/livingRoom/piscreen/power":
        # if value is true, shutdown Pi.
        manage_power(msg.payload.decode('UTF-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("<MosquittoIP>", <MosquittoPort>, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
