from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Articulos(Base):
    
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(50), ForeignKey("basico.idcvlac"), nullable=False)
    autores = Column(String(6000), nullable=False)
    nombre = Column(String(1500), nullable=False)
    tipo = Column(String(200), nullable=True)
    verificado = Column(Boolean,unique=False, default=True)
    lugar = Column(String(1000), nullable=True)
    revista = Column(String(1000), nullable=True)
    issn = Column(String(500), nullable=True)
    editorial = Column(String(1000), nullable=True)
    volumen = Column(String(100), nullable=True)
    fasciculo = Column(String(100), nullable=True)
    paginas = Column(String(80), nullable=True)
    fecha = Column(String(80), nullable=True)
    doi = Column(String(1000), nullable=True)
    palabras = Column(String(4000), nullable=True)
    sectores = Column(String(5000), nullable=True)
    
    basico = relationship('Basico', backref='articulos')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Articulos({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac