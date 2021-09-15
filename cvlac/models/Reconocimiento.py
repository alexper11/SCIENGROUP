from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Reconocimiento(Base):
    
    __tablename__ = 'reconocimiento'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(300), nullable=False)
    fecha = Column(String(80), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Reconocimiento({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac