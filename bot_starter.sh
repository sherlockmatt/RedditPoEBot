#!/bin/bash
## Simple shell script that reboots the bot if it crashes

## First check if the oauth.ini file exists. Else, run the setup.  
if [ ! -f /tmp/foo.txt ]; then
    echo "Running setup."
	python setup.py
fi

echo "Running bot."
until python redditbot.py; do
	echo "CRASH" >&2
	sleep 1
done
