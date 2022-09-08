from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, Boolean

class Articulos(Base):
    
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    verificado = Column(Boolean,unique=False, default=True)
    tipo = Column(String(200), nullable=True)
    nombre = Column(String(1500), nullable=False)
    lugar = Column(String(1000), nullable=True)
    revista = Column(String(1000), nullable=True)
    issn = Column(String(500), nullable=True)
    fecha = Column(String(80), nullable=True)
    volumen = Column(String(80), nullable=True)
    fasciculo = Column(String(80), nullable=True)
    paginas = Column(String(80), nullable=True)
    doi = Column(String(1000), nullable=True)
    autores = Column(String(6000), nullable=False)       
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Articulos({self.nombre}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac