import mariadb
import sys
import pandas as pd

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

data = pd.read_sql_query("SELECT * FROM devices;", conn)

for index, row in data.iterrows():
    print(row["plug"])

conn.close()
