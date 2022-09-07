from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class Lineas(Base):
    
    __tablename__ = 'lineas'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    lineas = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Lineas({self.idgruplac})'
    
    def __str__(self):
        return self.idcvlac