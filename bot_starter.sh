#!/bin/bash
## Simple shell script that reboots the bot if it crashes
echo "Running bot."
until python redditbot.py; do
	echo "CRASH" >&2
	sleep 1
done
