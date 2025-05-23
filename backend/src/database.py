from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from sqlalchemy import MetaData
from models import BlenderAsset

connection_string = "sqlite:///../../data/db1.db"
#connection_string = "mysql+mysqlconnector://root:secret@mysql:3306/store"
engine = create_engine(connection_string, echo = True)

def create_tables():
    metadata = MetaData()
    metadata.create_all(engine)

def drop_tables():
    metadata = MetaData()
    metadata.drop_all(engine)

def insert_blender_asset(name, filename):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj = BlenderAsset(name=name, filename=filename)
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj

def delete_blender_asset(asset_id: int):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj = session.query(BlenderAsset).get(asset_id)
        session.delete(obj)
        session.commit()

def update_blender_asset(asset_id, name, filename):
    obj = BlenderAsset.query.get(asset_id)
    if not obj: return
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj.name = name
        obj.filename = filename
        session.commit()

def get_blender_asset(asset_id=None):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(BlenderAsset)
        if asset_id:
            result = query.get(asset_id)
        else:
            result = query.all()
    return result
    
def insert_blender_asset_meshes(asset_id, meshes):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        asset = session.query(BlenderAsset).get(asset_id)
        #for mesh in meshes:
        #    asset.add