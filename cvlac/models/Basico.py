from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Basico(Base):
    
    __tablename__ = 'basico'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    categoria = Column(String(200), nullable=True)
    nombre = Column(String(200), nullable=False)
    nombre_citaciones = Column(String(200), nullable=True)
    nacionalidad = Column(String(100), nullable=True)
    sexo = Column(String(50), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Basico({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac