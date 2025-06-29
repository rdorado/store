import os
from random import randint

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image

from models import Category, Asset
import database
import blender_utils

from settings import check_folders, get_blender_folder, create_data_folder, get_renders_folder, get_thumbs_folder

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

@app.get("/category/type/{type}")
async def get_category_by_type(type: int):
    return database.get_category_by_type(Category, type)

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
    asset = database.get_model(Asset, asset_id)
    blender_folder = get_blender_folder()
    file_path = os.path.join(blender_folder, asset.filename)
    os.remove(file_path)
    return database.delete_model(Asset, asset_id)

@app.post("/asset")
async def create_asset(data: Asset):
    return database.insert_model(data)

@app.put("/asset")
async def update_asset(data: Asset):
    database.update_model(data)
    return {"result": "Success"}

def save_blender_file(blender_file):
    # Make file pattern
    filename = str(blender_file.filename)
    rdn = randint(100000, 999999)
    new_file_name = filename[:-6]+"_"+str(rdn)+".blend"

    # Prepare full path
    blender_folder = get_blender_folder()
    file_location = os.path.join(blender_folder, new_file_name)

    # Save file
    with open(file_location, "wb+") as file_object:
        file_object.write(blender_file.file.read())

    return new_file_name

def clip_image(image_filename):
    renders_folder = get_renders_folder()
    full_filename  = os.path.join(renders_folder, image_filename)
    image = Image.open(full_filename)
    width, height = image.size
    offset = (width - height)/2
    box = (offset, 0, width - offset, height)
    clipped_image = image.crop(box)
    clipped_image.save(full_filename)

def render_blender_file(blender_filename):
    check_folders()
    # Prepare blender file full path
    blender_folder = get_blender_folder()
    blender_filename_fullpath = os.path.join(blender_folder, blender_filename)

    # Prepare render image filename result full path
    renders_folder = get_renders_folder()
    image_filename = blender_filename[:-6]+".png"
    full_render_filename  = os.path.join(renders_folder, image_filename)
    blender_utils.render(blender_filename_fullpath, full_render_filename)
    clip_image(image_filename)

@app.post("/blender_asset/{asset_id}")
async def create_file(asset_id: int, blender_file: UploadFile = File(...)):
    # Save file in blender directory and change name into internal name
    new_file_name = save_blender_file(blender_file)

    # Update asset with blender internal filename and save into db
    asset = database.get_model(Asset, asset_id)
    asset.filename = new_file_name
    database.update_model(asset)

    render_blender_file(asset.filename)
    return {"result": "success"}

@app.get("/asset_categories/{asset_id}")
async def get_asset_categories(asset_id: int):
    return database.get_asset_categories(Category, asset_id)

@app.put("/asset_categories/{category_id}")
async def add_category_asset(data: Asset, category_id: int):
    database.add_category_to_asset(data.id, category_id)

@app.delete("/asset_categories/{category_id}")
async def remove_category_from_asset(data: Asset, category_id: int):
    database.remove_category_from_asset(data.id, category_id)

'''
**********************************
       IMAGES
**********************************
'''

def create_thumb(image_filename):
    thumbs_folder = get_thumbs_folder()
    thumb_full_filename  = os.path.join(thumbs_folder, image_filename)

    renders_folder = get_renders_folder()
    render_filename  = os.path.join(renders_folder, image_filename)
    image = Image.open(render_filename)

    maxsize = (80, 80)
    image.thumbnail(maxsize)
    image.save(thumb_full_filename)

@app.get("/img/")
async def get_image(id: int):
    asset = database.get_model(Asset, id)
    thumbs_folder = get_thumbs_folder()
    filename = asset.filename[:-6]+".png"
    thumb_filename  = os.path.join(thumbs_folder, filename)
    if not os.path.exists(thumb_filename):
        create_thumb(filename)
    return FileResponse(thumb_filename)


@app.get("/thumbnail")
async def thumbnail():
    return FileResponse("/data/thumbnail.png")
