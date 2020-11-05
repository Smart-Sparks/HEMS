MAC=sed "$1q;d" mac-lookup.txt
sudo rfcomm connect hci1 $(MAC) 1 &
