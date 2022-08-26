from cvlac.db import Base
from sqlalchemy import Column, Integer, String

class Libros(Base):
    
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    autores = Column(String(4000), nullable=False)
    nombre = Column(String(1000), nullable=False)
    lugar = Column(String(200), nullable=True)
    fecha = Column(String(20), nullable=True)
    editorial = Column(String(500), nullable=False)
    isbn = Column(String(500), nullable=True)
    volumen = Column(String(50), nullable=True)
    paginas = Column(String(50), nullable=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Libros({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac