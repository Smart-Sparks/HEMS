#Disconnect power to the load 
sudo bash connectsd.sh
sleep 1
sudo echo c >> /dev/rfcomm0 2>&1
