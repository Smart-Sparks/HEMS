#central_server.py

# START IMPORTS
import driveMethods as DM
from db_management import *
from time import sleep
# END IMPORTS

# START METHODS
# Looks every period in Google Drive, downloads all files there, and put them into database
def file_download_loop():
    wait_period = 2
    dbm = DatabaseManager()
    d = DM.access_drive()
    while (True):
        print('Checking Drive for files.')
        # Download Drive files to folder
        DM.download_all_files_from_folder_to_dir_recursively_then_delete_from_drive(
            d,
            'D:\\Documents\\GitRepos\\central-server\\v2\\centralCode\\downloaded_csvs',
            folder_id='root'
        )
        dbm.transfer_csvs_to_db()
        sleep(wait_period)

def main():
    file_download_loop()
# END METHODS

if __name__ == '__main__':
    main()