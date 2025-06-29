
import os

'''
Data folder
'''
data_folder = "../../data"
blender_folder = f"{data_folder}/blender"
images_folder = f"{data_folder}/images"
renders_folder = f"{images_folder}/renders"
thumbs_folder = f"{images_folder}/thumbs"

folders = [data_folder, blender_folder, images_folder, renders_folder, thumbs_folder]
'''
Connection string to the database. 

SQLite:
  connection_string = "sqlite:///../../data/db1.db"
Mysql:
  connection_string = "mysql+mysqlconnector://root:secret@mysql:3306/store"
'''
connection_string = f"sqlite:///{data_folder}/db1.db"

def get_data_folder():
    return data_folder

def get_blender_folder():
    return blender_folder

def get_renders_folder():
    return renders_folder

def get_thumbs_folder():
    return thumbs_folder

def create_data_folder():
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if not os.path.exists(blender_folder):
        os.makedirs(blender_folder)

def check_folders():
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)