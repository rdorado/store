from typing import List, Set

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String,Integer, ForeignKey, create_engine

from settings import connection_string, create_data_folder

class Base(DeclarativeBase):
    pass

class CategoryDAO(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[int] = mapped_column(Integer)

    assets: Mapped[List["AssetCategoryDAO"]] = relationship(back_populates="category")

class AssetDAO(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    filename: Mapped[str] = mapped_column(String(255))

    categories: Mapped[List["AssetCategoryDAO"]] = relationship(back_populates="asset")

class AssetCategoryDAO(Base):
    __tablename__ = "asset_category"
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), primary_key=True)

    asset: Mapped["AssetDAO"] = relationship(back_populates="categories")
    category: Mapped["CategoryDAO"] = relationship(back_populates="assets")

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

def get_asset_categories(modelclass, asset_id):
    Session = sessionmaker(bind=engine)
    result = []
    with Session() as session:
        query = session.query(modelclass.__daoclass__) \
                       .join(CategoryDAO.assets) \
                       .filter(AssetCategoryDAO.asset_id == asset_id)
        for category in query.all():
            result.append(modelclass.model_validate(category))
    return result

def add_category_to_asset(asset_id, category_id):
    Session = sessionmaker(bind=engine)
    assetCategory = None
    with Session() as session:
        assetCategory = AssetCategoryDAO()
        assetCategory.asset = session.get(AssetDAO, asset_id)
        assetCategory.category = session.get(CategoryDAO, category_id)
        session.add(assetCategory)
        session.commit()
    return assetCategory

def remove_category_from_asset(asset_id, category_id):
    Session = sessionmaker(bind=engine)
    assetCategory = None
    with Session() as session:
        assetCategory = session.get(AssetCategoryDAO, (asset_id, category_id))
        session.delete(assetCategory)
        session.commit()
    return assetCategory

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