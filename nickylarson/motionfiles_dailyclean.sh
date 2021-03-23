#!/bin/sh

logfile="/tmp/cleaning.log"
date=$(date)

echo "" >> "$logfile"
echo "$date" >> "$logfile"
echo "Cleaning old images" >> "$logfile"

sudo find /var/motion/pictures/ -mindepth 1 -mtime +4 -delete >> "$logfile" 2>&1

echo "Cleaning done" >> "$logfile"
echo "" >> "$logfile"
