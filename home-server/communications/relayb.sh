#Reconnect power to the load 
sudo bash ~/HEMS/home-server/communications/connectsd2.sh
sleep 1
sudo echo b >> /dev/rfcomm0 2>&1
