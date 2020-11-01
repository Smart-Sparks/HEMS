#db_management.py

# START IMPORTS
import sqlite3
import os
import pandas
import csv
# END IMPORTS

# START METHODS
def database_to_csv(db):
    db = 'D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\dbs\\data.db'
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute('select * from usage_data')
    with open('out.csv', 'w') as out:
        writer = csv.writer(out, delimiter=',')
        writer.writerow([i[0] for i in cur.description])
        writer.writerows(cur)
# END METHODS

# NOTES ON DATABASE LAYOUT:
# 2 TABLES USED:
#   'homes' table
#       Numbers home servers and keeps track of their unique GoogleDrive folder ids
#       homeid- int that increments
#       folderid- unique GD folder id from home
#   'data' table
#       Holds all data from all home servers
#       homeid- linked to specific home
#       time- datetime gathered by home server
#       irms- usage data
#       pwr- usage data
#       pf- usage data
#       energy- usage data



# START CLASSES
# Database Manager: Organizational unit to handle the transfer of data into
#                   a database from csv files.
class DatabaseManager:
    def __init__(self):
        self._data_table_name = 'data'
        self._temp_table_name = 'temp'
        self._csv_folder = 'D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\downloaded_csvs'
        self._database_file = 'D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\dbs\\data.db'

        self._data_cols_list = ['deviceid', 'time', 'irms', 'pwr', 'pf', 'energy', 'homeid']
        # self._data_cols_str = ', '.join(self._data_cols_list)
        self._data_col_types = ['INT', 'DATETIME', 'DOUBLE', 'DOUBLE', 'DOUBLE', 'DOUBLE', 'INT']

        self._temp_cols_list = ['deviceid', 'time', 'temperature', 'homeid']
        # self._temp_cols_str = ', '.join(self._temp_cols_list)
        self._temp_col_types = ['INT', 'DATETIME', 'DOUBLE', 'INT']



    # Periodically checks a local folder for any csv files
    def transfer_csvs_to_db(self):
        self.csv_folder_to_db(self._csv_folder, self._database_file)

    # recursively searches folder for csv files and transfers them to database
    def csv_folder_to_db(self, csvfolder, db):
        files = os.listdir(csvfolder)
        # print("checking csv folder: ", csvfolder)
        for file in files:
            # Get name of file
            absfile = os.path.join(csvfolder, file)
            ext = os.path.splitext(absfile)[1]
            # If file is a csv, then transfer it to database
            if ext == '.tsv':
                self.csvs_to_db([absfile], db)
            # If file is a subfolder, then recursively call this function on that folder
            elif os.path.isdir(absfile):
                self.csv_folder_to_db(absfile, db)

    # Takes list of csv file names and transfers them to a database
    def csvs_to_db(self, csvfiles, db):
        # For every csv file in the list of csv files
        for csv in csvfiles:
            # If the database exists, then put data from this file into the database
            if self.check_db_exists(db):
                print("db ", db, " exists")
                rc = self.csv_to_db(csv, db)
            # Otherwise, create the database before transferring data to it
            else:
                print("db ", db, " does not exist")
                self.create_db(db)
                rc = self.csv_to_db(csv, db)
            if rc == 0:     # Successful csv to db, csv can be deleted
                print("csv to db successful, deleting csv: ", csv)
                try:
                    os.remove(csv)
                except WindowsError as e:
                    print(e)
            # If return code of csv_to_db was not 0, then there was a problem
            else:
                print("Problem dumping ", csv, " to ", db)

    # Check if a path to certain database exists
    def check_db_exists(self, db_path):
        print("calling check_db_exists")
        if os.path.exists(db_path):
            return True
        else:
            return False

    # Creates an empty database if one is not there, and sets up columns
    def create_db(self, db_path):
        print("calling create_db")
        # Makes an empty db file
        open(db_path, 'a').close()
        # https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a
        # -sqlite3-database-table-using-python
        # Open database file
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        # Execute the instruction to create necessary table in database

        # OLD table creation
        # make_table_instr = "CREATE TABLE {tab} ({cols});".format(tab=self._table_name, cols=self._table_cols_str)

        # NEW table creation from script
        make_table_instr = open("db_init_homes_table.sql", "r").read()
        cur.execute(make_table_instr)
        make_table_instr = open("db_init_data_table.sql", "r").read()
        cur.execute(make_table_instr)
        make_table_instr = open("db_init_temp_table.sql", "r").read()
        cur.execute(make_table_instr)

        con.commit()
        con.close()

    # Uses pandas to transfer csv data to specified database
    # Should also add corresponding home server entry to 'homes' if needed
    def csv_to_db(self, csvfile, db_path):
        print("calling csv_to_db")
        # Checks if specified csv file exists at path
        if os.path.exists(csvfile):
            try:
                # open database
                con = sqlite3.connect(db_path)
                cur = con.cursor()

                # Checks if home server in 'homes' table
                file = os.path.split(csvfile)[1]
                filename = os.path.splitext(file)[0]
                folder_id = filename.split("---")[1]
                print("file is see in local folder: ", filename)
                print("extracted folderid:", folder_id)
                # Selects matching folder id from homes table if exists
                t = (folder_id,)
                cur.execute("SELECT * FROM homes WHERE folderid = ?", t)
                matching_homes = cur.fetchall()
                print(matching_homes)
                # Add home with folder id if none in db
                if len(matching_homes) == 0:
                    print("add home")
                    cur.execute("INSERT INTO 'homes' (folderid) VALUES(?);", t)
                cur.execute("SELECT * FROM homes WHERE folderid = ?", t)
                matching_homes = cur.fetchall()
                homeid = matching_homes[0][0]

                # Places csv data into 'data' or 'temp' table
                if (self.isUsageDataFile(filename)):
                    self.csvToDatabaseByDataframe(csvfile,
                                                  self._data_table_name,
                                                  self._data_cols_list,
                                                  self._data_col_types,
                                                  homeid,
                                                  con)
                elif (self.isTempDataFile(filename)):
                    self.csvToDatabaseByDataframe(csvfile,
                                                  self._temp_table_name,
                                                  self._temp_cols_list,
                                                  self._temp_col_types,
                                                  homeid,
                                                  con)
                else:
                    print(filename, " did not match usage pattern \"energy\" nor temperature pattern \"temperature\"")

                con.commit()
                con.close()
                return 0
            # Some errors could occur
            except sqlite3.Error as e:
                print("csv_to_db sqlite3 Error: ", e)
                return -1
            except OSError as e:
                print("csv_to_db OSError: ", e)
            except Exception as e:
                print("csv_to_db error: ", e)
        else:
            return -1

    def csvToDatabaseByDataframe(self, csvfile, table_name, col_list, col_types, homeid, sqlcon):
        # Read csv data into Pandas dataframe
        df = pandas.read_csv(csvfile, names=col_list, sep="\t")
        # Remove the header row
        df = df.drop(labels=[0], axis=0)
        # Fill homeid column with homeid
        df['homeid'] = homeid
        df['time'] = pandas.to_datetime(df['time'])
        # Make dict for dataframe to use for .to_sql
        print(df)
        dtype = {col_list[i]: col_types[i] for i in range(len(col_types))}
        # Append dataframe data to database
        df.to_sql(table_name, sqlcon, if_exists='append', index=False, dtype=dtype)

    def isUsageDataFile(self, filename):
        return filename.startswith("energy")

    def isTempDataFile(self, filename):
        return filename.startswith("temperature")
# END CLASSES