
#Takes the ID number as first cla $1
#sudo echo a > ~/HEMS/home-server/communications/testy.txt
~/HEMS/home-server/communications/connectsd.sh $1
sleep 5
echo $1 $(date '+%Y-%m-%d %H:%M:%S') > ~/HEMS/home-server/communications/SmartDevice$1.txt
sudo echo a >> /dev/rfcomm0 
sleep 1
sudo cat /dev/rfcomm0 >> ~/HEMS/home-server/communications/SmartDevice$1.txt 2>&1

#sudo tee SmartDevice$1.txt < /dev/rfcomm0
#cp /dev/rfcomm0 SmartDevice$1.txt 
#sleep 15
#echo Disconnecting...
#bash disconnect.sh 
#echo Writing to database...
#sudo python3 ../backend/write-data.py SmartDevice$1.txt
#echo Finished
