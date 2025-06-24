import os
from random import randint

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models import Category, Asset
import database

from settings import get_blender_folder, create_data_folder

allowed_cors_origins = [
   "http://localhost:4200",
   "http://localhost:4201",
   "http://localhost:8000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    message = "It works"
    return {"message": message}

'''   
**********************************
       Database management
**********************************
'''
@app.get("/db/create")
async def create_db():
    database.create_tables()
    return {"message": "Success"}

@app.get("/db/drop")
async def drop_db():
    database.drop_tables()
    return {"message": "Success"}

'''
**********************************
       Categories
**********************************
'''

@app.post("/category")
async def create_category(data: Category):
    database.insert_model(data)
    return {"result": "Success"}

@app.put("/category")
async def update_category(data: Category):
    database.update_model(data)
    return {"result": "Success"}

@app.get("/category")
async def get_category():
    return database.get_model(Category, None)

@app.delete("/category/{model_id}")
async def delete_category(model_id: int):
    database.delete_model(Category, model_id)
    return {"result": "Success"}

'''
**********************************
       Asset
**********************************
'''

@app.get("/asset")
async def get_asset():
    return database.get_model(Asset, None)

@app.delete("/asset/{asset_id}")
async def delete_asset(asset_id: int):
    return database.delete_model(Asset, asset_id)

@app.post("/asset")
async def create_asset(data: Asset):
    return database.insert_model(data)

@app.put("/asset")
async def update_asset(data: Asset):
    database.update_model(data)
    return {"result": "Success"}

@app.post("/blender_asset/{asset_id}")
async def create_file(asset_id: int, blender_file: UploadFile = File(...)):
    filename = str(blender_file.filename)
    if filename.endswith(".blend"):
        rdn = randint(1000, 9999)
        new_file_name = filename[:-6]+"_"+str(rdn)+".blend"
        data_folder = get_blender_folder()
        file_location = os.path.join(data_folder, new_file_name)
        create_data_folder()
        with open(file_location, "wb+") as file_object:
            asset = database.get_model(Asset, asset_id)
            asset.filename = new_file_name
            database.update_model(asset)
            file_object.write(blender_file.file.read())
    return {"result": "success"}

'''
**********************************
       TODO: refactor / delete
**********************************
'''

#@app.get("/img")
#async def image():
#    filename = blender_utils.render()
#    return FileResponse(filename)

@app.delete("/blender_asset/{asset_id}")
async def delete_blender_asset(asset_id: int):
    asset = database.get_blender_asset(asset_id)
    if asset:
        os.remove(asset.filename)
        database.delete_blender_asset(asset_id)

@app.get("/thumbnail")
async def thumbnail():
    return FileResponse("/data/thumbnail.png")

@app.get("/info")
async def info():
    file_location = "/data/test.blend"
    result = blender_utils.file_info(file_location)
    return {"result": result}

@app.get("/blender_asset/{asset_id}/meshes")
async def get_blender_asset_meshes(asset_id: int):
    pass
