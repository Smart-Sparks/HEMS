bash connectsd3.sh
# temperature sensor
sleep 5
echo 3 $(date '+%Y-%m-%d %H:%M:%S') > SmartDevice3.txt 2>&1
sudo echo a >> /dev/rfcomm0 2>&1
sleep 1
cat /dev/rfcomm0 >> SmartDevice3.txt 2>&1
sleep 15
bash disconnect.sh
