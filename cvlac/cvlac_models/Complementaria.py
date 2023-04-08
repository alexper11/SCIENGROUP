from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Complementaria(Base):
    
    __tablename__ = 'complementaria'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(50), ForeignKey("basico.idcvlac"), nullable=False)
    tipo = Column(String(500), nullable=True)
    institucion = Column(String(800), nullable=True)
    titulo = Column(String(1500), nullable=True)
    fecha = Column(String(500), nullable=True)
    
    basico = relationship('Basico', backref='complementaria')
    
    def __init__(self, **kwargs):
       
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Complementaria({self.tipo}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac