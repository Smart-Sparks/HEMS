#!/usr/bin/bash
echo Collecting data from SmartDevice1
bash connectsd1.sh
sleep 5
echo 1 $(date '+%Y-%m-%d %H:%M:%S') > SmartDevice1.txt
sudo echo a >> /dev/rfcomm0 2>&1
sleep 1
sudo cat /dev/rfcomm0 >> SmartDevice1.txt 2>&1
#sleep 15
bash disconnect.sh 
echo Finished sd1.sh
