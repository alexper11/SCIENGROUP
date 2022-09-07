from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String

class Jurados(Base):
    
    __tablename__ = 'jurados'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(1000), nullable=False)
    titulo = Column(String(1000), nullable=False)
    tipo = Column(String(500), nullable=True)
    lugar = Column(String(200), nullable=True)
    programa = Column(String(800), nullable=True)
    orientado = Column(String(1500), nullable=True)
    palabras = Column(String(3000), nullable=True)
    areas = Column(String(3000), nullable=True)
    sectores = Column(String(3000), nullable=True)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Jurados({self.nombre}, {self.idcvlac}, {self.titulo})'
    
    def __str__(self):
        return self.idcvlac