from typing import Optional
from pydantic import BaseModel, ConfigDict
from database import CategoryDAO, AssetDAO

class DataModel(BaseModel):
    __daoclass__ = None
    model_config = ConfigDict(from_attributes=True)

class Category(DataModel):
    __daoclass__ = CategoryDAO

    id: Optional[int] = None
    name: str
    type: int

class Asset(DataModel):
    __daoclass__ = AssetDAO

    id: Optional[int] = None
    name: str
    filename: Optional[str] = None

