#!/bin/sh

logfile="/tmp/watcher.log"
date=$(date)

which inotifywait >/dev/null || err "you need 'inotifywait' command (sudo apt-get install inotify-tools )"
pkill -f "inotifywait -m /var/motion/pictures -e create -e moved_to" # kill old watcher

inotifywait -m /var/motion/pictures -e create -e moved_to |
    while read path action file; do
        #echo "The file '$file' appeared in directory '$path' via '$action'"
        echo "" >> "$logfile"
        echo "$date" >> "$logfile"
        scp "$path$file" user@server:/path/to/backups/ >> "logfile" 2>&1
        echo "Copying new files $file" >> "$logfile"
    done
