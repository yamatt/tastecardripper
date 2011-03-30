#!/bin/sh

python tastecardRipper.py -c config.json > ~/tcrip.`date +%Y-%m-%dT%H:%M:%S`.log
