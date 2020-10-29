# home_server.py

# START IMPORTS
import driveMethods as DM
import os
from time import sleep
import configparser
import pathlib
from os.path import join
# END IMPORTS

# START METHODS
def upload_file_to_drive(f, folder_id):
    #info_file = "hs_info.txt"
    #config = configparser.ConfigParser()
    #config.read(info_file)
    #folder_id = config.get('home server', 'folder_id')

    d = DM.access_drive()
    # r = DM.upload_csv_to_drive(d, f)
    r = DM.upload_csv_to_drive_folder(d, f, folder_id)
    return r

def delete_local_csv(f):
    os.remove(f)

# Loops and checks folder every period, uploading csv files in the folder and deleting when successful
def file_check_loop(in_folder, folder_id):
    data_src_dir = in_folder
    wait_period = 2
    # Should loop forever
    while (True):
        files = os.listdir(data_src_dir)
        print(files)
        # attempts to upload every .csv in src folder, deletes files of any other type
        for file in files:
            f = os.path.join(data_src_dir, file)
            ext = os.path.splitext(f)[1]
            if ext == '.tsv':
                print("here")
                # attempts upload and deletes file on success
                ret = upload_file_to_drive(f, folder_id)
                print(ret)
                if (ret == 0):
                    delete_local_csv(f)
            else:
                os.remove(f)
        sleep(wait_period)


def main():
    print("Start Home Server")
    #info_file = "hs_info.txt"
    info_file = os.path.join(pathlib.Path(__file__).parent.absolute(), "hs_info.txt")
    config = configparser.ConfigParser()
    config.read(info_file)
    in_folder = config.get('home server', 'input')
    in_folder = os.path.join(pathlib.Path.home(), in_folder)
    folder_id = config.get('home server', 'folder_id')
    file_check_loop(in_folder, folder_id)
# END METHODS


if __name__ == '__main__':
    main()
