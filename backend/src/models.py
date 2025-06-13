from typing import Optional
from pydantic import BaseModel, ConfigDict
from database import CategoryDAO

class Category(BaseModel):
    __daoclass__ = CategoryDAO
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str
    type: int

'''
class Asset(Base):
    __tablename__ = "asset"

    #id = Column(Integer, primary_key = True)
    #name = Column(String(255))
    #filename = Column(String(255))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    filename: Mapped[str] = mapped_column(String(255))
    #meshes: Mapped[List["BlenderAssetMesh"]] = relationship()
    
    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.filename


class BlenderAssetMesh(Base):
    __tablename__ = "asset_mesh"

    #id = Column(Integer, primary_key = True)
    #name = Column(String(255))
    id: Mapped[int] = mapped_column(primary_key=True)
    #asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"))
    name: Mapped[str] = mapped_column(String(255))
    
    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.filename
'''