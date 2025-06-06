
import os

'''
Connection string to the database. 

SQLite:
  connection_string = "sqlite:///../../data/db1.db"
Mysql:
  connection_string = "mysql+mysqlconnector://root:secret@mysql:3306/store"
'''
connection_string = "sqlite:///../../data/db1.db"

'''
Data folder
'''
data_folder = "../../data"


def create_data_folder():
    print(data_folder)
    print(os.path.exists(data_folder))
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)