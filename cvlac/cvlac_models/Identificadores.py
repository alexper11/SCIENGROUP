from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Identificadores(Base):
    
    __tablename__ = 'identificadores'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), ForeignKey("basico.idcvlac"), nullable=False)
    nombre = Column(String(1000), nullable=True)
    url = Column(String(1000), nullable=True)
    
    basico = relationship('Basico', backref='identificadores')
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Identificadores({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac