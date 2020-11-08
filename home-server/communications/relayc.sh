#Disconnect power to the load 
sudo bash ~/HEMS/home-server/communications/connectsd2.sh
sleep 1
sudo echo c >> /dev/rfcomm0 2>&1
