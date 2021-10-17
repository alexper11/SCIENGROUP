from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Articulos(Base):
    
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    autores = Column(String(250), nullable=False)
    nombre = Column(String(300), nullable=False)
    lugar = Column(String(50), nullable=True)
    revista = Column(String(340), nullable=True)
    issn = Column(String(12), nullable=True)
    editorial = Column(String(360), nullable=True)
    volumen = Column(String(10), nullable=True)
    fasciculo = Column(String(30), nullable=True)
    paginas = Column(String(10), nullable=True)
    fecha = Column(String(30), nullable=True)
    doi = Column(String(250), nullable=True)
    palabras = Column(String(600), nullable=True)
    sectores = Column(String(1000), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Articulo({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac