# send to /homeBackend/input
# datetime=`date +"%D%T" -R`
datetime=`date -R | tr -d :,./ | tr -d [:blank:]`
fileprefix=${datetime:3:-5}
PATHNAME=~/homeBackend/input/
echo ${PATHNAME}${fileprefix}devices.tsv
( echo 'SELECT * FROM devices' | sudo mariadb -B hems ) > ${PATHNAME}${fileprefix}devices.tsv
( echo 'SELECT * FROM energy' | sudo mariadb -B hems ) > ${PATHNAME}${fileprefix}energy.tsv
( echo 'SELECT * FROM temperature' | sudo mariadb -B hems ) > ${PATHNAME}${fileprefix}temperature.tsv
