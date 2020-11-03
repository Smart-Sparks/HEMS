bash connectsd3.sh
# temperature sensor
sleep 5
cat /dev/rfcomm0 > SmartDevice3.txt 2>&1
