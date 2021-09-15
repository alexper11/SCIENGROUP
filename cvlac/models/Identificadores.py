from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Identificadores(Base):
    
    __tablename__ = 'identificadores'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(300), nullable=False)
    url = Column(String(300), nullable=False)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Identificadores({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac