from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Libros(Base):
    
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    autores = Column(String(4000), nullable=True)
    nombre = Column(String(1000), nullable=True)
    tipo = Column(String(150), nullable=True)
    verificado = Column(Boolean,unique=False, default=True)
    lugar = Column(String(200), nullable=True)
    fecha = Column(String(80), nullable=True)
    editorial = Column(String(500), nullable=True)
    isbn = Column(String(500), nullable=True)
    volumen = Column(String(100), nullable=True)
    paginas = Column(String(50), nullable=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    basico = relationship('Basico', backref='libros')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Libros({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac