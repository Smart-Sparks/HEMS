#!/usr/bin/bash
# William Plucknett
# Pull all of the data out of the hems database and write them in
# separate .tsv files for Chase's central server to pick up.

# send to /homeBackend/input
# datetime=`date +"%D%T" -R`
newtime=`date +"%F %T"`
datetime=`date -R | tr -d :,./ | tr -d [:blank:]`
fileaffix=${datetime:3:-5}
PATHNAME=~/homeBackend/input/
prevuploadfile=~/HEMS/home-server/backend/prevdatetime.txt
prevdatevar=$(cat ${prevuploadfile})
echo Writing .tsv files to ${PATHNAME} with affix ${fileaffix}.
( echo "SELECT * FROM devices" | sudo mariadb -B hems ) > ${PATHNAME}devices${fileaffix}.tsv
echo Wrote devices table.
( echo "SELECT * FROM energy WHERE time > '${prevdatevar}'" | sudo mariadb -B hems ) > ${PATHNAME}energy${fileaffix}.tsv
echo Wrote energy table.
( echo "SELECT * FROM temperature WHERE time > '${prevdatevar}'" | sudo mariadb -B hems ) > ${PATHNAME}temperature${fileaffix}.tsv
echo Wrote temperature table.
echo ${newtime} > ${preuploadfile}
