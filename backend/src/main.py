from random import randint

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import Category
import database

allowed_cors_origins = [
   "http://localhost:4200",
   "http://localhost:4201",
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
    #message = blender_utils.render()
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

@app.get("/thumbnail")
async def thumbnail():
    return FileResponse("/data/thumbnail.png")

@app.get("/info")
async def info():
    file_location = "/data/test.blend"
    result = blender_utils.file_info(file_location)
    return {"result": result}

'''
**********************************
       Blender asset
**********************************
'''

#@app.get("/img")
#async def image():
#    filename = blender_utils.render()
#    return FileResponse(filename)

@app.post("/blender_asset")
async def create_file(blender_file: UploadFile = File(...)):
    filename = str(blender_file.filename)
    if filename.endswith(".blend"):
        rdn = randint(1000, 9999)
        file_location = filename[:-6]+"_"+str(rdn)+".blend"
        with open(file_location, "wb+") as file_object:
            file_object.write(blender_file.file.read())
            blender_asset = database.insert_blender_asset(name=filename, filename=file_location)
        meshes = blender_utils.get_meshes_from_asset(file_location)
        database.insert_blender_asset_meshes(blender_asset, meshes)
    return {"result": "success"}

'''
@app.post("/blender_asset")
async def create_file(data):
    print(data)
'''

@app.delete("/blender_asset/{asset_id}")
async def delete_blender_asset(asset_id: int):
    asset = database.get_blender_asset(asset_id)
    if asset:
        os.remove(asset.filename)
        database.delete_blender_asset(asset_id)

@app.get("/blender_asset/get") 
async def get_blender_asset():
    return database.get_blender_asset(None)

@app.get("/blender_asset/{asset_id}/meshes")
async def get_blender_asset_meshes(asset_id: int):
    pass


