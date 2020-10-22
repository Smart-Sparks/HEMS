import mariadb
import pandas as pd
import calculations as calc

datafile = r'datafile.csv'

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
    preamble = [preamble[0], preamble[1], preamble[2]+' '+preamble[3]] # reconcatenate the datetime
    #print(preamble)
device_id = int(preamble[0])                # device id that uploaded data
num_rows = int(preamble[1])                 # number of rows of data
time_updated = preamble[2].replace('"', '') # time the device uploaded data to the server

df = pd.read_csv (datafile, header=None, skiprows=[0], names=['time','power','pf','rms current'])
print(df)
# calculate energy per row
df['energy'] = [calc.energy(power, pf) for power, pf in zip(df['power'],df['pf'])]

# write to mariadb
try:
    cur.execute("INSERT INTO devices (id, last_update) VALUES (?, ?)",
            (device_id, time_updated))
except mariadb.Error as e:
    print(f"Error: {e}")
    sys.exit(2)
for idx in range(num_rows):
    row = df.iloc[idx]
    cur.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)",
            (device_id,
                row['time'], row['power'], row['pf'], row['rms current'], row['energy']) 
            )
conn.commit()
conn.close()
