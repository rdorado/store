
import os

'''
Data folder
'''
data_folder = "../../data"
blender_folder = f"{data_folder}/blender"

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

def create_data_folder():
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if not os.path.exists(blender_folder):
        os.makedirs(blender_folder)
