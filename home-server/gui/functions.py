###################
#FUNCTIONS for GUI#
###################

import mariadb
import sys

#connectMDB returns the connection
#maybe should move this to a class that closes the connection upon the destruction occurring?
def connectMDB():
    try: 
        conn = mariadb.connect(user='root', password='', host='localhost', database='hems')
        conn.autocommit = False
        print("Successfully connected to the database.")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

