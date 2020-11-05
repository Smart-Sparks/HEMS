
#Takes the ID number as first cla $1
./connectsd.sh $1
sleep 5
echo 1 $(date '+%Y-%m-%d %H:%M:%S') > SmartDevice$1.txt
sudo echo a >> /dev/rfcomm0 2>&1
sleep 1
sudo cat /dev/rfcomm0 >> SmartDevice$1.txt 2>&1
sleep 15
bash disconnect.sh 

