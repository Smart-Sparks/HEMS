#Reconnect power to the load 
sudo bash connectsd2.sh
sleep 1
sudo echo b >> /dev/rfcomm0 2>&1
