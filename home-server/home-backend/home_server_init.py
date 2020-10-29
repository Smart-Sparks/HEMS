# home_server_init.py

# START IMPORTS
import driveMethods as DM
import os
import configparser
from time import sleep
# END IMPORTS


def check_drive_for_id(id):
    d = DM.access_drive()
    DM.print_file_list(d)
    folders = DM.get_folder_list(d)
    all_ids = [int(folder['title']) for folder in folders]
    # if folder with id name is not in the drive, then make a new folder for it
    # with id of 1 greater than current largest
    if not all_ids:
        all_ids = [0]
    if id not in all_ids:
        # new id is one greater than the current greatest id
        new_id = max(all_ids[:]) + 1
        # Create new folder for this home server on the drive
        new_folder_name = str(new_id)
        new_folder = d.CreateFile({'title': new_folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        new_folder.Upload()
        # Save the id for the folder
        new_folder_id = new_folder['id']
        return new_id, new_folder_id
    return id, None


def main():
    info_file = "hs_info.txt"
    config = configparser.ConfigParser()
    config.read(info_file)
    id = config.getint('home server', 'id')
    in_folder = config.get('home server', 'input')
    token_file = config.get('home server', 'token')
    # If this home server hasn't been initialized and gotten an id, then do so
    if (id == -1):
        new_id, new_folder_id = check_drive_for_id(id)
        # successfully get new id
        if new_id > -1:
            # write new home id and folder id (on the drive) to the info file
            config['home server']['id'] = str(new_id)
            config['home server']['folder_id'] = str(new_folder_id)
            with open(info_file, 'w') as newinfo:
                config.write(newinfo)


if __name__ == "__main__":
    main()