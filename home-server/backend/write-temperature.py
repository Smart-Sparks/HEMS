import mariadb
import pandas as pd
import calculations as calc
import sys
import datetime as dt

# TODO: TAKE AS CLA
#datafile = r'../communications/SmartDevice3.txt'
datafile = r'temperaturefile.csv'

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
num_rows = int(antepreabmle[0]) # number of rows of data
time_millis = int antepreamble[1] # time the arduiono plug/temp sensor uploaded data (in millis() function format)

df = pd.read_csv (datafile, header=None, skiprows=[0], names=['time','temperature'])
print(df)

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
