#driveMethods.py

# START IMPORTS
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pydrive.files
import os
# END IMPORTS

# START METHODS
def access_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def print_file_list(drive):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print('Files in Drive')
    for f in file_list:
        print('title: %s, id: %s' % (f['title'], f['id']))
# END METHODS

# START METHODS
# uploads file @ csv_path to the GoogleDrive object, drive
# returns 0 on successfule upload, -1 if problem
def upload_csv_to_drive(drive, csv_path):
    try:
        file1 = drive.CreateFile({'title': 'data.csv'})
        file1.SetContentFile(csv_path)
        file1.Upload()
        return 0
    except pydrive.files.ApiRequestError:
        # problem with Upload()
        return -1

# uploads file @ csv_path to the GoogleDrive object at folder, drive
# returns 0 on successfule upload, -1 if problem
def upload_csv_to_drive_folder(drive, csv_path, folder_id):
    try:
        file1 = drive.CreateFile({'title': 'data.csv', 'parents': [{"id": folder_id}]})
        file1.SetContentFile(csv_path)
        file1.Upload()
        return 0
    except pydrive.files.ApiRequestError:
        # problem with Upload()
        return -1

# Downloads all non-trashed files from the specified GoogleDrive
def download_all_files_from_root(drive):
    # Get list of all non-trashed files
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for f in file_list:
        # pyDrive's CreateFile + GetContentFile downloads the file to folder where this is run from
        fd = drive.CreateFile({'title': f['title'], 'id': f['id']})
        fd.GetContentFile(f['title'])
        print('title: %s, id: %s' % (f['title'], f['id']))

# Downloads all non-trashed files from the specified GoogleDrive to a specific directory
def download_all_files_from_root_to_directory(drive, dir):
    # Get list of all non-trashed files
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for f in file_list:
        try:
            # Create file from Drive using id
            fd = drive.CreateFile({'title': f['title'], 'id': f['id']})
            orig_file, ext = os.path.splitext(f['title'])
            # Add id to filename for download
            filename = orig_file + "_" + f['id'] + ext
            # Downloads file with new filename in specified directory
            fd.GetContentFile(os.path.join(dir, filename))
            print('title: %s, id: %s' % (f['title'], f['id']))
        # Some errors may occur
        except pydrive.files.ApiRequestError:
            pass
        except pydrive.files.FileNotUploadedError:
            pass
        except pydrive.files.FileNotDownloadableError:
            pass

# Downloads all non-trashed files from the specified GoogleDrive to a specific
# directory then delete those files from the Drive
def download_all_files_from_root_to_dir_then_delete_from_drive(drive, dir):
    # Get list of all non-trashed files
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    for f in file_list:
        try:
            # Create file from Drive using id
            fd = drive.CreateFile({'title': f['title'], 'id': f['id']})
            orig_file, ext = os.path.splitext(f['title'])
            # Add id to filename for download
            filename = orig_file + "_" + f['id'] + ext
            # Downloads file with new filename in specified directory
            fd.GetContentFile(os.path.join(dir, filename))
            # Delete file from GoogleDrive
            fd.Delete()
            print('title: %s, id: %s' % (f['title'], f['id']))
        # Some errors may occur
        except pydrive.files.ApiRequestError:
            pass
        except pydrive.files.FileNotUploadedError:
            pass
        except pydrive.files.FileNotDownloadableError:
            pass


def download_all_files_from_folder_to_dir_recursively_then_delete_from_drive(drive, dir, folder_id='root'):
    # Get list of all non-trashed files
    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    # For every file found (this includes folders)
    for f in file_list:
        # if the file is a folder, call this again on that folder
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            download_all_files_from_folder_to_dir_recursively_then_delete_from_drive(drive, dir, f['id'])
        # if it is a file, then just try to download and delete it from drive
        else:
            try:
                # Create file from Drive using id
                fd = drive.CreateFile({'title': f['title'], 'id': f['id']})
                orig_file, ext = os.path.splitext(f['title'])

                # Add id to filename for download
                # filename = orig_file + "_" + f['id'] + ext
                # Create title with parent folder id in name
                filename = orig_file + "---" + folder_id + ext

                # Downloads file with new filename in specified directory
                fd.GetContentFile(os.path.join(dir, filename))
                # Delete file from GoogleDrive
                fd.Delete()
                print('title: %s, id: %s' % (f['title'], f['id']))
            # Some errors may occur
            except pydrive.files.ApiRequestError:
                pass
            except pydrive.files.FileNotUploadedError:
                pass
            except pydrive.files.FileNotDownloadableError:
                pass




def get_folder_list(drive):
    file_list = drive.ListFile(
        {'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    return file_list
# END METHODS