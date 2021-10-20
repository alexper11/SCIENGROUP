from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Estancias(Base):
    
    __tablename__ = 'estancias'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(600), nullable=True)
    entidad = Column(String(200), nullable=True)
    area = Column(String(600), nullable=True)
    fecha_inicio = Column(String(100), nullable=True)
    fecha_fin = Column(String(100), nullable=True)
    descripcion=Column(String(2000), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Estancias({self.tipo}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac