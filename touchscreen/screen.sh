#!/bin/bash

STATE=$1

if [ "$1" = "on" ]; then
	#echo "turning on screen"
	sudo rpi-backlight --on
elif [ "$1" = "off" ]; then
	#echo "turning off screen"
	sudo rpi-backlight --off
fi
