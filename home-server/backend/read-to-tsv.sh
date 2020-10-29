# send to /homeBackend/input
#datetime=`date +"%D %T"`
PATHNAME="~/homeBackend/input/"
`echo 'SELECT * FROM devices' | mysql -B hems` > ${PATHNAME}devices.tsv
`echo 'SELECT * FROM energy' | mysql -B hems` > ${PATHNAME}energy.tsv
`echo 'SELECT * FROM temperature' | mysql -B hems` > ${PATHNAME}temperature.tsv
