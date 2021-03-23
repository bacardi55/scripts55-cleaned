#!/bin/bash

# This script is run after the event starts.

logfile="/tmp/alert.log"
date=$(date)

echo "" >> "$logfile"
echo "$date" >> "$logfile"
echo "Motion event started" >> "$logfile"

# Get home mode.
echo "Starting alert" >> "$logfile"
mode=$(curl -s -X GET http://<NoderedIP>:<NoderedPort>/api/home/mode | jq -r ".house_mode")

echo "current house mode: $mode" >> "$logfile"

if [ -z "$mode" ]; then
    mode="empty"
fi

# If mode is not manual or full, raise an alert
if [ "$mode" != "full" ] && [ "$mode" != "Manual" ]; then
    # Retrieve latest video:
    mosquitto_pub -h <MosquittoIP> -p <MosquittoPort> -t home/entry/motion -m 1 -q 2
fi
