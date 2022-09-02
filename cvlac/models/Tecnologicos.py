from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Tecnologicos(Base):
    
    __tablename__ = 'tecnologicos'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    autor = Column(String(4000), nullable=False)
    nombre = Column(String(1000), nullable=False)
    tipo = Column(String(500), nullable=False)
    contrato_registro = Column(String(300), nullable=True)
    lugar = Column(String(50), nullable=True)
    fecha = Column(String(500), nullable=False)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Tecnologicos({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac