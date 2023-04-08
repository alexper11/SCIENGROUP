from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Lineas(Base):
    
    __tablename__ = 'lineas'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), ForeignKey("basico.idgruplac"), nullable=False)
    lineas = Column(String(3000), nullable=True)
    
    basico = relationship('Basico', backref='lineas')
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Lineas({self.idgruplac})'
    
    def __str__(self):
        return self.idgruplac