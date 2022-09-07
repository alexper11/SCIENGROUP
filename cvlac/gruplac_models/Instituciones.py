from cvlac.db_gruplac import Base
from sqlalchemy import Column, Integer, String

class Instituciones(Base):
    
    __tablename__ = 'instituciones'
    id = Column(Integer, primary_key=True)
    idgruplac = Column(String(50), nullable=False)
    nombre = Column(String(400), nullable=True)
    aval = Column(String(50), nullable=True)
    
    def __init__(self, **kwargs):
    
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Basico({self.nombre}, {self.idcvlac})'
    
    def __str__(self):
        return self.idcvlac