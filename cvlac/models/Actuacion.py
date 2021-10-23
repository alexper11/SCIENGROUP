from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Actuacion(Base):
    
    __tablename__ = 'actuacion'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(1000), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Actuacion({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac