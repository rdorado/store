from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import create_engine, String, Integer

from settings import connection_string, create_data_folder

class Base(DeclarativeBase):
    pass

class CategoryDAO(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[int] = mapped_column(Integer)

class AssetDAO(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    filename: Mapped[str] = mapped_column(String(255))

engine = create_engine(connection_string, echo = True)

'''
**********************************
       Database management
**********************************
'''

def create_tables():
    create_data_folder()
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)

'''
**********************************
       Generic Models
**********************************
'''

def insert_model(model):
    data = model.__daoclass__(**model.dict())
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.add(data)
        session.commit()
        session.refresh(data)
    return data

def update_model(model):
    Session = sessionmaker(bind=engine)
    catDAO = None
    with Session() as session:
        query = session.query(model.__daoclass__)
        data = query.get(model.id)
        for field in data.__table__.columns.keys():
            if field not in data.__table__.primary_key.columns.keys():
                setattr(data, field, getattr(model, field))
        session.commit()
    return catDAO

def delete_model(modelclass, model_id):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(modelclass.__daoclass__)
        data = query.get(model_id)
        session.delete(data)
        session.commit()

def get_model(modelclass, model_id=None):
    Session = sessionmaker(bind=engine)
    result = None
    with Session() as session:
        query = session.query(modelclass.__daoclass__)
        if model_id:
            result = modelclass.model_validate(query.get(model_id))
        else:
            result = []
            for model in query.all():
                result.append(modelclass.model_validate(model))
    return result

'''
**********************************
       Asset
**********************************
'''

def insert_blender_asset(name, filename):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj = Asset(name=name, filename=filename)
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj

def delete_blender_asset(asset_id: int):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj = session.query(Asset).get(asset_id)
        session.delete(obj)
        session.commit()

def update_blender_asset(asset_id, name, filename):
    obj = Asset.query.get(asset_id)
    if not obj: return
    Session = sessionmaker(bind=engine)
    with Session() as session:
        obj.name = name
        obj.filename = filename
        session.commit()

"""
def get_blender_asset(asset_id=None):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(Asset)
        if asset_id:
            result = query.get(asset_id)
        else:
            result = query.all()
    return result
"""
    
def insert_blender_asset_meshes(asset_id, meshes):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        asset = session.query(Asset).get(asset_id)
        #for mesh in meshes:
        #    asset.add