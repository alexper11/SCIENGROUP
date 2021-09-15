from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Complementaria(Base):
    
    __tablename__ = 'complementaria'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    tipo = Column(String(50), nullable=False)
    institucion = Column(String(300), nullable=True)
    area = Column(String(300), nullable=True)
    fecha = Column(String(100), nullable=True)
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Complementaria({self.tipo}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac