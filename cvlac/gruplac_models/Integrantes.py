from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Integrantes(Base):
    
    __tablename__ = 'integrantes'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    url = Column(String(1000), nullable=True)
    integrante = Column(String(400), nullable=True)
    vinculacion = Column(String(80), nullable=True)
    horas = Column(String(20), nullable=True)
    fecha_vinculacion = Column(String(250), nullable=True)
    
    basico = relationship('Basico', backref='integrantes')
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Integrantes({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac