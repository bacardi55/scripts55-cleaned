#!/bin/bash

# This script is run after the event end.

logfile="/tmp/alert.log"
date=$(date)

echo "" >> "$logfile"
echo "$date" >> "$logfile"

# Get home mode.
echo "Event end alert" >> "$logfile"
mode=$(curl -s -X GET http://<NoderedIP>:<NoderedPort>/api/home/mode | jq -r ".house_mode")

echo "current house mode: $mode" >> "$logfile"

if [ -z "$mode" ]; then
    mode="empty"
fi

# If mode is not manual or full, raise an alert
if [ "$mode" == "Away" ]; then
    # Retrieve latest video:
    file=$(ls -t /var/motion/pictures/*.mp4 | head -1)
    curl -X POST  http://<NoderedIP>:<NoderedPort>/api/home/entry/camera/event/end -F "file=@$file" > /dev/null 2>&1
fi
