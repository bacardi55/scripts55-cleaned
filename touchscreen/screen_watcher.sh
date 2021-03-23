#!/bin/sh

which inotifywait >/dev/null || err "you need 'inotifywait' command (sudo apt-get install inotify-tools )"
pkill -f "inotifywait -q -m -e close_write /home/pi/node-red/data/screen_watcher" # kill old watcher

inotifywait -q -m -e close_write /home/pi/node-red/data/screen_watcher |
while read -r filename event; do
  status=$(/bin/cat /home/pi/node-red/data/screen_watcher)
  if [ "$status" = "1" ]; then
    #echo "turning screen on!"
    /bin/sh /home/pi/scripts/screen.sh on
  elif [ "$status" = "0" ]; then
    #echo "turning screen off!"
    /bin/sh /home/pi/scripts/screen.sh off
  fi

  # echo "changing file to false"
  echo "-1" > /home/pi/node-red/data/screen_watcher
  sleep 1

done
