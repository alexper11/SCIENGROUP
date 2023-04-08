from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String

class Basico(Base):
    
    __tablename__ = 'basico'
    #id = Column(Integer, primary_key=True)
    idcvlac = Column(String(50), primary_key=True)
    categoria = Column(String(500), nullable=True)
    nombre = Column(String(1000), nullable=False)
    nombre_citaciones = Column(String(1000), nullable=True)
    nacionalidad = Column(String(500), nullable=True)
    sexo = Column(String(200), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Basico({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac