# William Plucknett
# Pull all of the data out of the hems database and write them in
# separate .tsv files for Chase's central server to pick up.

# send to /homeBackend/input
# datetime=`date +"%D%T" -R`
datetime=`date -R | tr -d :,./ | tr -d [:blank:]`
fileaffix=${datetime:3:-5}
PATHNAME=~/homeBackend/input/
echo Writing .tsv files to ${PATHNAME} with affix ${fileaffix}.
( echo 'SELECT * FROM devices' | sudo mariadb -B hems ) > ${PATHNAME}devices${fileaffix}.tsv
( echo 'SELECT * FROM energy' | sudo mariadb -B hems ) > ${PATHNAME}energy${fileaffix}.tsv
( echo 'SELECT * FROM temperature' | sudo mariadb -B hems ) > ${PATHNAME}temperature${fileaffix}.tsv
