bash connectsd2.sh
sleep 5
echo 2 $(date '+%Y-%m-%d %H:%M:%S') > SmartDevice2.txt 2>&1
sudo echo a >> /dev/rfcomm0 2>&1
sleep 1
sudo cat /dev/rfcomm0 >> SmartDevice2.txt 2>&1
sleep 15
bash disconnect.sh 
