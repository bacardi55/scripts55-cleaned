#!/bin/sh

which inotifywait >/dev/null || err "you need 'inotifywait' command (sudo apt-get install inotify-tools )"
pkill -f "inotifywait -q -m -e close_write /home/pi/node-red/data/reboot_kalliope" # kill old watcher

inotifywait -q -m -e close_write /home/pi/node-red/data/reboot_kalliope |
while read -r filename event; do
  status=$(/bin/cat /home/pi/node-red/data/reboot_kalliope)
  if [ "$status" = "true" ]; then
    # echo "rebooting kalliope"
    /bin/sh /home/pi/kalliope_config/scripts/restart-kalliope.sh

    sleep 1

    # echo "changing file to false"
    echo "false" > /home/pi/node-red/data/reboot_kalliope
  fi
done
