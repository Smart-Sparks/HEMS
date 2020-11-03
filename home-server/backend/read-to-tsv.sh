# send to /homeBackend/input
#datetime=`date +"%D %T"`
PATHNAME="~/homeBackend/input/"
`echo 'SELECT * FROM devices' | sudo mariadb -B hems` > "${PATHNAME}devices.tsv"
`echo 'SELECT * FROM energy' | sudo mariadb -B hems` > "${PATHNAME}energy.tsv"
`echo 'SELECT * FROM temperature' | sudo mariadb -B hems` > "${PATHNAME}temperature.tsv"
