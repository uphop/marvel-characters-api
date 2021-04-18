from sqlalchemy import Column, String, Table, DateTime
from sqlalchemy.orm import relationship, backref
from data.models.meta import Base

class Character(Base):
    __tablename__ = "character"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    modified = Column(DateTime)
    thumbnail_path = Column(String)
    thumbnail_extension = Column(String)

    def __init__(self, id, name, description, modified, thumbnail_path, thumbnail_extension):
        self.id = id
        self.name = name
        self.description = description
        self.modified = modified
        self.thumbnail_path = thumbnail_path
        self.thumbnail_extension = thumbnail_extension
