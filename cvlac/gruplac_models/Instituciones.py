from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Instituciones(Base):
    
    __tablename__ = 'instituciones'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    nombre = Column(String(400), nullable=True)
    aval = Column(String(50), nullable=True)
    
    basico = relationship('Basico', backref='instituciones')  
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Instituciones({self.nombre}, {self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac