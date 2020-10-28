bash connectsd3.sh
sleep 5
echo "01" > /dev/rfcomm0
sudo cat /dev/rfcomm0 > testresults.txt 2>&1


