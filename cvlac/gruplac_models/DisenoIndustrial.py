from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class DisenoIndustrial(Base):
    
    __tablename__ = 'diseno_industrial'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    verificado = Column(Boolean,unique=False, default=True)
    tipo = Column(String(200), nullable=True)
    nombre = Column(String(1500), nullable=True)
    lugar = Column(String(200), nullable=True)
    fecha = Column(String(100), nullable=True)
    disponibilidad = Column(String(100), nullable=True)
    institucion = Column(String(800), nullable=True)
    autores = Column(String(6000), nullable=True)       
    
    basico = relationship('Basico', backref='diseno_industrial') 
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'DisenoIndustrial({self.nombre}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac