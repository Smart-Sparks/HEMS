# takes the file as the first argument
import mariadb
import pandas as pd
import calculations as calc
import sys
import datetime as dt

datafile = r'../communications/SmartDevice2.txt' # make CLA

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
time_millis = int antepreamble[1] # time the arduino plug/temp sensor uploaded data (in millis() function format)

df = pd.read_csv (datafile, header=None, skiprows=[0,1], names=['time','power','pf','rms current'])
print(df)

# calculate energy per row
df['energy'] = [calc.energy(power, pf) for power, pf in zip(df['power'],df['pf'])]
# convert the time in millis into datetime type
time_updated_DT = dt.datetime.strptime(time_updated, "%Y-%m-%d %H:%M:%S") # python datetime format
df['time'] = [(time_updated_DT - dt.deltaTime(milliseconds = millis)) for millis in df['time']]

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
