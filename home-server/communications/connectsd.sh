#!/bin/bash
# $1 is the line of the mac-lookup.txt to pull from
echo "Connecting to Device with ID $1"
echo `sed "$1q;d" ./mac-lookup.txt`
MAC=`sed "$1q;d" ./mac-lookup.txt`
sudo rfcomm connect hci1 $(MAC) 1 &
