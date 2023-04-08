from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Estancias(Base):
    
    __tablename__ = 'estancias'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    nombre = Column(String(1000), nullable=True)
    entidad = Column(String(500), nullable=True)
    area = Column(String(1500), nullable=True)
    fecha_inicio = Column(String(200), nullable=True)
    fecha_fin = Column(String(200), nullable=True)
    descripcion=Column(String(3000), nullable=True)
    
    basico = relationship('Basico', backref='estancias')
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Estancias({self.tipo}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac