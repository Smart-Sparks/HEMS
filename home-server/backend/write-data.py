# William Plucknett
# This file should be called as python3 write-data.py DATAFILENAME {TEMPERATURE/ENERGY}
import mariadb
import pandas as pd
import calculations as calc
import sys
import datetime as dt

#########
# SETUP #
#########

# check command line arguments
if len(sys.argv) != 3:
    print(f"Improper usage of this script.")
    print(f"Proper usage: python3 {str(sys.argv[0])} DATAFILE TYPE")
    print("Where DATAFILE is the name of the datafile and TYPE is whether it is temperature or energy data.")
    sys.exit(1)

datafile = str(sys.argv[1])

#mariadb connection
try: 
    conn = mariadb.connect(user='root', password='', host='localhost', database='hems')
    conn.autocommit = False
    print("Successfully connected to the database.")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
# get cursor
cur = conn.cursor()

with open(datafile, 'r') as data:
    preamble = data.readline().split()
    preamble = [preamble[0], preamble[1]+' '+preamble[2]] # reconcatenate the datetime
    antepreamble = data.readline().split()
    #print(preamble)
device_id = int(preamble[0])                # device id that uploaded data
time_updated = preamble[1].replace('"', '') # time the device uploaded data to the server
num_rows = int(antepreamble[0]) # number of rows of data
Tx_millis = int(antepreamble[1]) # time the arduino plug/temp sensor uploaded data (in millis() function format)



###################
# IF ENERGY FILE #
##################
if(str(sys.argv[2]) == "ENERGY"):
    df = pd.read_csv (datafile, header=None, skiprows=[0,1], names=['time','power','pf','rms current'])
    print(df)

# calculate energy per row
    df['energy'] = [calc.energy(power, pf) for power, pf in zip(df['power'],df['pf'])]
# convert the time in millis into datetime type
    time_updated_DT = dt.datetime.strptime(time_updated, "%Y-%m-%d %H:%M:%S") # python datetime format
    df['time'] = [str(time_updated_DT - dt.timedelta(milliseconds=(Tx_millis - millis))) for millis in df['time']] # milliseconds=(Tx_millis - millis) finds how long ago the data was measured in ms

# write to mariadb
    try: 
        cur.execute("REPLACE INTO devices (id, last_update, plug) VALUES (?, ?, ?)",
                (device_id, time_updated, True))
    except mariadb.Error as e:
        print(f"Error: {e}")
        sys.exit(2)
    for idx in range(num_rows):
        row = df.iloc[idx]
        cur.execute("INSERT INTO energy VALUES (?, ?, ?, ?, ?, ?)",
                (device_id,
                    row['time'], row['power'], row['pf'], row['rms current'], row['energy']) 
                )
    conn.commit()
    conn.close()
#######################
# IF TEMPERATURE FILE #
#######################
elif(str(sys.argv[2] == "TEMPERATURE")):
    df = pd.read_csv (datafile, header=None, skiprows=[0], names=['time','temperature'])
    print(df)

# convert the time in millis into datetime type
    time_updated_DT = dt.datetime.strptime(time_updated, "%Y-%m-%d %H:%M:%S") # python datetime format
    df['time'] = [str(time_updated_DT - dt.timedelta(milliseconds=(Tx_millis - millis))) for millis in df['time']] # milliseconds=(Tx_millis - millis) finds how long ago the data was measured in ms
# write to mariadb
    try:
        cur.execute("REPLACE INTO devices (id, last_update, plug) VALUES (?, ?, ?)",
                (device_id, time_updated, False))
    except mariadb.Error as e:
        print(f"Error: {e}")
        sys.exit(2)
    for idx in range(num_rows):
        row = df.iloc[idx]
        cur.execute("INSERT INTO temperature VALUES (?, ?, ?)",
                (device_id,
                    row['time'], row['temperature']) 
                )
    conn.commit()
    conn.close()
##############
# UKNOWN FILE#
##############
else:
    print("ERROR: COULD NOT PROPERLY READ FILE. IMPROPER FORMAT GIVEN IN argv[2].")
    print("The second argument should be either TEMPERATURE or ENERGY.")
    sys.exit(1)
sys.exit(0)
