#!/bin/bash
## Simple shell script that reboots the bot if it crashes

prefix="[$(date +"%Y-%m-%d %H:%M:%S")] "

echo $prefix + "Running bot."
until python redditbot.py; do
	echo $prefix + "CRASH" >&2
	sleep 1
done
