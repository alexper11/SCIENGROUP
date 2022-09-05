from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

class MetaDB(Base):
    
    __tablename__ = 'metadb'
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(timezone=True), default=func.now())
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
